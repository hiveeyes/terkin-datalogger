# -*- coding: utf-8 -*-
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2019-2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# License: GNU General Public License, Version 3
import time
import machine

from __main__ import bootloader
from umal import ApplicationInfo, PlatformInfo

from terkin import __version__
from terkin import logging
from terkin.exception import SensorUnknownError
from terkin.configuration import TerkinConfiguration
from terkin.device import TerkinDevice
from terkin.network import SystemWiFiMetrics
from terkin.sensor import SensorManager, AbstractSensor
from terkin.model import SensorReading, DataFrame
from terkin.sensor.system import SystemMemoryFree, SystemTemperature, SystemVoltage, SystemUptime
from terkin.util import gc_disabled

log = logging.getLogger(__name__)


class TransientStorage:
    """
    Store last sensor reading for serving through HTTP API.
    """

    def __init__(self):
        self.last_reading = {}


# Maybe refactor to TerkinCore.
class TerkinDatalogger:
    """ 
    Main class of project.
    Handles loop & sleep, registers sensors, reads their data and stores them.
    Shows up as 'datalogger' in the rest of the program.
    """

    # Application metadata.
    name = 'Terkin Datalogger'
    version = __version__

    # For the singleton factory.
    __instance__ = None

    def __init__(self, settings, platform_info: PlatformInfo = None):

        # Reference to the chronometer used for general timekeeping.
        self.duty_chrono = bootloader.duty_chrono

        # Signal startup with first available timestamp.
        log.info('Starting Terkin datalogger')

        # Obtain configuration settings.
        self.settings = TerkinConfiguration()
        self.settings.add(settings)
        self.settings.add_user_file()

        # Configure logging.
        logging_enabled = self.settings.get('main.logging.enabled', False)
        if not logging_enabled:
            log.info('Disabling logging to save bytes')
            logging.disable_logging()

        # Initialize ApplicationInfo object.
        self.application_info = ApplicationInfo(
            name=self.name, version=self.version, settings=self.settings,
            application=self, platform_info=platform_info)

        # Initialize transient storage.
        self.storage = TransientStorage()

        # Initialize device.
        self.device = TerkinDevice(self.application_info)

        # Button manager instance (optional).
        self.button_manager = None

        # Initialize sensor domain.
        self.sensor_manager = SensorManager(self.settings)

    def setup(self):

        # Report about wakeup reason and run wakeup tasks.
        self.device.resume()

        # Start the watchdog for sanity.
        self.device.watchdog.start()

        # Configure RGB-LED according to settings.
        self.device.configure_rgb_led()

        # Alternative startup signalling: 2 x green.
        self.device.blink_led(0x000b00, count=2)

        # Free up some memory.
        self.device.run_gc()

        # Turn off LTE modem and Bluetooth as we don't use them yet.
        # TODO: Make this configurable.
        has_lte_modem = self.application_info.platform_info.device_name in ['GPy', 'FiPy']
        lte_enabled = self.settings.get('networking.lte.enabled')
        if has_lte_modem and not lte_enabled:
            self.device.power_off_lte_modem()

        self.device.power_off_bluetooth()

        log.info('Starting %s', self.application_info.fullname)

        # Dump configuration settings.
        log_configuration = self.settings.get('main.logging.configuration', False)
        if log_configuration:
            self.settings.dump()

        # Disable this if you don't want serial access.
        #self.device.enable_serial()

        # Hello world.
        self.device.print_bootscreen()

        # Start networking and telemetry subsystems.

        # Conditionally start network services and telemetry if networking is available.
        try:
            self.device.start_networking()
        except Exception as ex:
            log.exc(ex, 'Networking subsystem failed')
            self.device.status.networking = False

        self.device.start_telemetry()

        # Todo: Signal readyness by publishing information about the device (Microhomie).
        # e.g. ``self.device.publish_properties()``

        self.setup_sensors()

    def setup_sensors(self):

        # Setup sensors.
        log.info('Setting up sensors')
        self.device.watchdog.feed()
        bus_settings = self.settings.get('sensors.buses', self.settings.get('sensors.busses', []))
        self.sensor_manager.setup_buses(bus_settings)
        self.register_sensors()
        self.sensor_manager.start_sensors()

        log.info('Setup finished')

    def start(self):
        self.start_mainloop()

    def start_mainloop(self):
        """ """

        # Todo: Refactor by using timers.

        # Enter the main loop.
        while True:
            self.duty_task()

    def duty_task(self):
        """Main duty cycle task."""

        # Feed the watchdog timer to keep the system alive.
        self.device.watchdog.feed()

        # Indicate activity.
        # Todo: Optionally disable this output.
        log.info('--- cycle ---')

        # Run downstream mainloop handlers.
        self.duty_cycle()

        # Sleep how ever.
        self.sleep()

    def duty_cycle(self):
        """Main duty cycle"""

        if not self.settings.get('main.deepsleep', False):
            self.duty_chrono.reset()

        #log.info('Terkin loop')

        # Alternative loop signalling: 1 x blue.
        # https://forum.pycom.io/topic/2067/brightness-of-on-board-led/7
        self.device.blink_led(0x00000b, count=2)

        # Read sensors.
        readings = self.read_sensors()

        # Remember current reading
        self.storage.last_reading = readings.data_in

        # Run the garbage collector.
        self.device.run_gc()

        # Transmit data.
        transmission_success = self.transmit_readings(readings)

        # Signal transmission outcome.
        if transmission_success:
            self.device.blink_led(0x00000b)
        else:
            self.device.blink_led(0x0b0000)

        # Run the garbage collector.
        self.device.run_gc()

        # Give the system some breath.
        machine.idle()

    def sleep(self):
        """Sleep until the next measurement cycle."""

        lightsleep = self.settings.get('main.lightsleep', False)
        deepsleep = self.settings.get('main.deepsleep', False)
        interval = self.get_sleep_time()

        # Amend deep sleep intent when masked through maintenance mode.
        if self.device.status.maintenance is True:
            lightsleep = False
            deepsleep = False
            log.info('Device is in maintenance mode. Skipping deep sleep and '
                     'adjusting sleep time to {} seconds.'.format(interval))

        # Prepare device shutdown.
        try:

            # Shut down sensor peripherals.
            self.sensor_manager.power_off()

            # Shut down networking.
            if deepsleep:
                self.device.networking.stop()

        except Exception as ex:
            log.exc(ex, 'Power off failed')

        # Activate device sleep mode.
        try:
            self.device.hibernate(interval, lightsleep=lightsleep, deepsleep=deepsleep)

        # When hibernation fails, fall back to regular "time.sleep".
        except Exception as ex:
            log.exc(ex, 'Failed to hibernate, falling back to regular sleep')
            # Todo: Emit error message here.
            log.info('Sleeping for {} seconds'.format(interval))
            time.sleep(interval)

    def get_sleep_time(self):
        """ 
        Calculate the next sleep intervall.
        """

        interval = self.settings.get('main.interval', 60.0)

        # Configuration switchover backward compatibility / defaults.
        if isinstance(interval, (float, int)):
            self.settings.set('main.interval', {})
            self.settings.setdefault('main.interval.field', interval)
        self.settings.setdefault('main.interval.maintenance', 5.0)

        interval = self.settings.get('main.interval.field')

        # First, try to acquire deep sleep interval from NVRAM.
        # This gets used when set from a LoRaWAN downlink message.
        # pycom.nvs_get should return "None" in case of unset key. Instead it throws an error
        try:
            import pycom
            interval_minutes = pycom.nvs_get('deepsleep')
            if isinstance(interval_minutes, int):
                log.info('Deep sleep interval set to %s minute(s) by LoRaWAN downlink message', interval_minutes)
                interval = interval_minutes * 60

        # Otherwise, use original configuration setting.
        except Exception as ex:
            pass

        # Amend deep sleep intent when masked through maintenance mode.
        if self.device.status.maintenance is True:
            interval = self.settings.get('main.interval.maintenance')

        # Compute sleeping duration from measurement interval and elapsed time.
        elapsed = self.duty_chrono.read()
        sleep_time = interval - elapsed

        if sleep_time <= 0:
            sleep_time = interval

        return sleep_time

    def register_sensors(self):
        """
        Configure and register sensor objects.
        There are three types of sensors: system, environment & buses.

        The sensors are registered by calling their respective classes
        from terkin/driver.

        Definitions are in 'settings.py'.
        """

        # Add sensors.
        log.info('Registering sensors')
        sensor_infos = []

        # Get list of system sensors from configuration settings.
        sensor_infos += self.settings.get('sensors.system', [])

        # Get list of environmental sensors from configuration settings.
        sensor_infos += self.settings.get('sensors.environment', [])

        # Backward compatibility for environmental sensors.
        if sensor_infos is None:
            sensor_infos += self.settings.get('sensors.registry', {}).values() or []

        # Scan sensor definitions, create and register sensor objects.
        for sensor_info in sensor_infos:

            sensor_type = sensor_info.get('type', 'unknown').lower()
            sensor_id = sensor_info.get('id', sensor_info.get('key', sensor_type))

            # Skip sensor if disabled in configuration.
            if not sensor_info.get('enabled', False):
                log.debug('Sensor with id={} and type={} is disabled, skipping registration'.format(sensor_id, sensor_type))
                continue

            # Skip WiFi sensor registration when WiFi is disabled.
            if sensor_type == 'system.wifi':
                if not self.settings.get('networking.wifi.enabled'):
                    log.info('WiFi is disabled, skipping sensor registration')
                    continue

            self.register_sensor(sensor_info)

            # Clean up memory after creating each sensor object.
            #self.device.run_gc()

    def register_sensor(self, sensor_info):
        """
        Register one sensor.
        """
        sensor_type = sensor_info.get('type', 'unknown').lower()
        sensor_id = sensor_info.get('id', sensor_info.get('key', sensor_type))
        description = sensor_info.get('description')

        # Resolve associated bus object.
        sensor_bus = None
        sensor_bus_name = None
        if 'bus' in sensor_info:
            sensor_info_bus = sensor_info['bus']
            sensor_bus = self.sensor_manager.get_bus_by_name(sensor_info_bus)

            # Skip sensor if associated bus is disabled in configuration.
            if sensor_bus is None:
                log.info('Bus {} for sensor with id={} and type={} is disabled, '
                         'skipping registration'.format(sensor_info_bus, sensor_id, sensor_type))
                return
            sensor_bus_name = sensor_bus.name

        # Human readable sensor address.
        if 'address' in sensor_info:
            sensor_address = hex(sensor_info.get('address'))
        else:
            sensor_address = None

        # Report sensor registration to user.
        message = 'Setting up sensor with id={} and type={} on bus={} with address={}'.format(
            sensor_id, sensor_type, sensor_bus_name, sensor_address)
        if description:
            message += ' described as "{}"'.format(description)
        log.info(message)

        # Backward compat.
        if sensor_type == 'ds18b20':
            sensor_type = 'ds18x20'

        # Registration NG
        # Run self-registration procedure by invoking
        # the "includeme()" function on each sensor module.
        try:

            # Load sensor module.
            import terkin.driver
            modulename = '{}_sensor'.format(sensor_type)
            fullname = 'terkin.driver.{}'.format(modulename)
            log.info('Importing module "{}"'.format(fullname))
            __import__(fullname)
            module = getattr(terkin.driver, modulename)

            # Acquire sensor object.
            includeme = getattr(module, 'includeme')
            sensor_object = includeme(self.sensor_manager, sensor_info)

            # Register sensor with sensor manager.
            self.sensor_manager.register_sensor(sensor_object)

            return

        except ImportError as ex:
            if not fullname.startswith('terkin.driver.system'):
                log.error('Driver module "{}" not found'.format(fullname))

        except AttributeError as ex:
            if "has no attribute 'includeme'" in str(ex):
                log.warning('Driver module "{}" is deprecated, "includeme" is missing'.format(fullname))
            else:
                log.exc(ex, 'Driver module "{}" failed'.format(fullname))

        except Exception as ex:
            log.exc(ex, 'Registering driver module "{}" failed'.format(fullname))

        # Legacy registration
        try:
            self.register_sensor_legacy(sensor_info, sensor_bus)
        except Exception as ex:
            log.exc(ex, 'Setting up sensor with id={} and type={} failed'.format(sensor_id, sensor_type))

    def register_sensor_legacy(self, sensor_info, sensor_bus):

        sensor_type = sensor_info.get('type', 'unknown').lower()

        # Sensor reporting about free system memory.
        if sensor_type == 'system.memfree':
            sensor_object = SystemMemoryFree(sensor_info)

        # Sensor which reports system temperature.
        elif sensor_type == 'system.temperature':
            sensor_object = SystemTemperature(sensor_info)

        # Sensor which reports battery voltage.
        elif sensor_type in ['system.voltage.battery', 'system.battery-voltage']:
            sensor_object = SystemVoltage(sensor_info)

        # Sensor which reports solar panel voltage.
        elif sensor_type == 'system.voltage.solar':
            sensor_object = SystemVoltage(sensor_info)

        # Sensor which reports system uptime metrics.
        elif sensor_type == 'system.uptime':
            sensor_object = SystemUptime(sensor_info)

        # Sensor which reports WiFi metrics.
        elif sensor_type == 'system.wifi':
            try:
                sensor_object = SystemWiFiMetrics(sensor_info, self.device.networking.wifi_manager.station)
            except Exception as ex:
                log.exc(ex, 'Enabling SystemWiFiMetrics sensor failed')
                return

        # Initialize buttons / touch pads.
        elif sensor_type == 'system.touch-buttons':
            from terkin.sensor.button import ButtonManager
            self.button_manager = ButtonManager()
            self.start_buttons()
            return

        else:
            raise SensorUnknownError('Unknown sensor type "{}"'.format(sensor_type))

        # Register sensor object with sensor manager.
        self.sensor_manager.register_sensor(sensor_object)

    def read_sensors(self) -> DataFrame:
        """
        Read measurements from all sensor objects that have been registered in the sensor_manager.
        Reading is done with the read() function of each respective sensor object.
        """

        # Power up sensor peripherals.
        self.sensor_manager.power_on()

        # Collect observations.
        data = {}
        richdata = {}
        readings = []

        # Iterate all registered sensors.
        sensors = self.sensor_manager.sensors
        log.info('Reading %s sensor ports', len(sensors))
        for sensor in sensors:

            # Signal sensor reading to user.
            sensorname = sensor.__class__.__name__
            log.info('Reading sensor port "%s"', sensorname)

            # Read sensor port.
            try:

                # Disable garbage collector to guarantee reasonable
                # realtime behavior before invoking sensor reading.
                with gc_disabled():
                    sensor_outcome = sensor.read()

                # Power off HX711 after reading
                if "HX711Sensor" in sensorname:
                   sensor.power_off()

                # Backward compat.
                if isinstance(sensor_outcome, SensorReading):
                    sensor_reading = sensor_outcome
                else:
                    sensor_reading = SensorReading()
                    sensor_reading.sensor = sensor
                    sensor_reading.data = sensor_outcome

                sensor_data = sensor_reading.data

                # Evaluate sensor outcome.
                if sensor_data is None or sensor_data is AbstractSensor.SENSOR_NOT_INITIALIZED:
                    continue

                # Round values according to sensor settings.
                if sensor.settings.get('decimals') is not None:
                    for key, value in sensor_data.items():
                        sensor_data[key] = round(sensor_data[key], sensor.settings.get('decimals'))

                # Add sensor reading to observations.
                data.update(sensor_data)

                # Record reading for prettified output.
                self.record_reading(sensor, sensor_data, richdata)

                readings.append(sensor_reading)

            except Exception as ex:
                # Because of the ``gc_disabled`` context manager used above,
                # the propagation of exceptions has to be tweaked like that.
                log.exc(ex, 'Reading sensor "%s" failed', sensorname)

            # Feed the watchdog.
            self.device.watchdog.feed()

            # Clean up memory after reading each sensor object.
            #self.device.run_gc()

        # Debugging: Print sensor data before running telemetry.
        prettify_log = self.settings.get('sensors.prettify_log', False)
        if prettify_log:
            from terkin.util import ddformat
            log.info('Sensor data:\n\n%s', ddformat(richdata, indent=11))
        else:
            log.info('Sensor data:  %s', data)

        # Capture all sensor readings.
        result = DataFrame()
        result.readings = readings
        result.data_in = data

        return result

    def record_reading(self, sensor, reading, richdata):
        """

        :param sensor: 
        :param reading: 
        :param richdata: 

        """
        for key, value in reading.items():
            richdata[key] = {'value': value}
            if hasattr(sensor, 'settings') and 'description' in sensor.settings:
                richdata[key]['description'] = sensor.settings.get('description')
                # Hack to propagate the correct detail-description to prettified output.
                # TODO: Attach settings directly to its reading, while actually reading it.
                if 'devices' in sensor.settings:
                    for device_settings in sensor.settings['devices']:
                        device_address = device_settings['address'].lower()
                        if device_address in key:
                            if hasattr(sensor, 'get_device_description'):
                                device_description = sensor.get_device_description(device_address)
                                if device_description:
                                    richdata[key]['description'] = device_description

    def transmit_readings(self, dataframe: DataFrame):
        """
        Transmit data

        :param dataframe:

        """

        # TODO: Optionally disable telemetry.
        if self.device.telemetry is None:
            log.warning('Telemetry disabled')
            return False

        telemetry_status = self.device.telemetry.transmit(dataframe)
        count_total = len(telemetry_status)
        success = all(telemetry_status.values())

        # Evaluate telemetry status outcome.
        if success:
            log.info('Telemetry status: SUCCESS ({}/{})'.format(count_total, count_total))
        else:
            count_failed = len([item for item in telemetry_status.values() if item is not True])
            log.warning('Telemetry status: FAILURE. {} out of {} targets failed. '
                        'Status: {}'.format(count_failed, count_total, telemetry_status))

        return success

    def start_buttons(self):
        """
        Configure ESP32 touchpads.
        """

        # RGB-LED: 2
        # POWER-ENABLE: 3
        # SD-Card: 4, 8
        # LTE 19, 20
        # Misc: 13, 14, 9, 23

        # Physical location when looking at the board with the RGB-LED oriented to the top.

        # Location: Left side, 6th pin from top.
        self.button_manager.setup_touchpad('P4', name='Touch3', location='Module-Left-Top-6th')

        # Location: Left side, 5th pin from bottom.
        self.button_manager.setup_touchpad('P8', name='Touch2', location='Module-Left-Bottom-5th')

        # Location: Right side.
        self.button_manager.setup_touchpad('P23', name='Touch6', location='Module-Right-Top-4th')

        # Location: Right side.
        # ValueError: invalid pin for touchpad
        """
        P18 and P17 are able to wake up on rising and falling edge. These two pins have internal
        pull-ups configurable by software (Pull-downs if needed must be added externally)

        -- https://docs.pycom.io/gitbook/assets/deepsleep-pinout.pdf


        ext0 External Wake-up Source
        RTC controller contains logic to trigger wake-up when one particular pin is set to
        a predefined logic level. That pin can be one of RTC GPIOs 0,2,4,12-15,25-27,32-39.

        -- https://lastminuteengineers.com/esp32-deep-sleep-wakeup-sources/#ext0-external-wakeup-source

        """
        #self.button_manager.setup_touchpad('P17', name='TouchX', location='Module-Right-Bottom-5th')
        #self.button_manager.setup_touchpad('P18', name='TouchY', location='Module-Right-Bottom-6th')

        # Will yield ``ValueError: Touch pad error``.
        #self.button_manager.setup_touchpad('P20', name='Touch8', location='Module-Right-Top-7th')
        #self.button_manager.setup_touchpad('P19', name='Touch9', location='Module-Right-Top-8th')

    def scale_wizard(self):
        """
        Invoke scale adjustment wizard.

        Synopsis:

        - Invoke Terkin datalogger.
        - Interrupt by pressing CTRL+C.
        - Type ``datalogger.scale_wizard()``.
        """

        # Setup sensors.
        self.setup_sensors()

        # Invoke scale adjustment routine.
        from terkin.sensor.scale import ScaleAdjustment
        adj = ScaleAdjustment(sensor_manager=self.sensor_manager)
        adj.start_wizard()
