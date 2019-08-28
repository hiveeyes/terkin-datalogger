# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import machine
from terkin import __version__
from terkin import logging
from terkin.configuration import TerkinConfiguration
from terkin.device import TerkinDevice
from terkin.network import SystemWiFiMetrics
from terkin.sensor import SensorManager, AbstractSensor
from terkin.sensor.system import SystemMemoryFree, SystemTemperature, SystemBatteryLevel, SystemUptime
from terkin.util import dformat, gc_disabled, ddformat

log = logging.getLogger(__name__)


class ApplicationInfo:

    def __init__(self, name=None, version=None, settings=None, application=None, platform_info=None):

        self.name = name
        self.version = version

        self.platform_info = platform_info

        self.settings = settings
        self.application = application

    @property
    def fullname(self):
        return '{} {}'.format(self.name, self.version)


class TransientStorage:

    def __init__(self):
        self.last_reading = {}


# Maybe refactor to TerkinCore.
class TerkinDatalogger:

    # Application metadata.
    name = 'Terkin MicroPython Datalogger'
    version = __version__

    # For the singleton factory.
    __instance__ = None

    def __init__(self, settings, platform_info=None):

        # Fulfill singleton factory.
        TerkinDatalogger.__instance__ = self

        # Obtain configuration settings.
        self.settings = TerkinConfiguration()
        self.settings.add(settings)

        self.application_info = ApplicationInfo(
            name=self.name, version=self.version, settings=self.settings,
            application=self, platform_info=platform_info)

        # Configure logging.
        logging_enabled = self.settings.get('main.logging.enabled', False)
        if not logging_enabled:
            log.info('Disabling logging to save bytes')
            logging.disable_logging()

        # Initialize transient storage.
        self.storage = TransientStorage()

        # Initialize device.
        self.device = TerkinDevice(self.application_info)

        # Button manager instance (optional).
        self.button_manager = None

        # Initialize sensor domain.
        self.sensor_manager = SensorManager()

    @staticmethod
    def getInstance(settings=None):
        """
        Singleton factory.
        """
        if TerkinDatalogger.__instance__ is None:
            if settings is None:
                raise Exception("Settings are None but instance wasn't created before.")
            else:
                TerkinDatalogger(settings)

        return TerkinDatalogger.__instance__

    def setup(self):
        pass

    def start(self):

        # Report about wakeup reason and run wakeup tasks.
        self.device.resume()

        # Start the watchdog for sanity.
        self.device.watchdog.start()

        # Configure RGB-LED according to settings.
        self.device.configure_rgb_led()

        # Alternative startup signalling: 2 x green.
        self.device.blink_led(0x000b00, count=2)

        # Turn off LTE modem and Bluetooth as we don't use them yet.
        # Todo: Revisit where this should actually go.
        # The modem driver takes about six seconds to initialize, so adjust the watchdog accordingly.
        self.device.watchdog.reconfigure_minimum_timeout(15000)
        if not self.settings.get('main.fastboot', False):
            self.device.power_off_lte_modem()
        self.device.power_off_bluetooth()
        self.device.watchdog.resume()

        log.info('Starting %s', self.application_info.fullname)

        # Dump configuration settings.
        log_configuration = self.settings.get('main.logging.configuration', False)
        if log_configuration:
            self.settings.dump()

        # Initialize buttons / touch pads.
        buttons_enabled = self.settings.get('sensors.system.buttons.enabled', False)
        if buttons_enabled:
            from terkin.sensor.button import ButtonManager
            self.button_manager = ButtonManager()
            self.start_buttons()

        # Disable this if you don't want serial access.
        #self.device.enable_serial()

        # Hello world.
        self.device.print_bootscreen()

        # Start networking and telemetry subsystems.

        # Conditionally start network services and telemetry if networking is available.
        try:
            self.device.start_networking()
        except Exception:
            log.exception('Networking subsystem failed')
            self.status.networking = False

        self.device.start_telemetry()

        # Todo: Signal readyness by publishing information about the device (Microhomie).
        # e.g. ``self.device.publish_properties()``

        # Setup sensors.
        self.device.watchdog.feed()
        bus_settings = self.settings.get('sensors.busses')
        self.sensor_manager.setup_busses(bus_settings)
        self.register_sensors()

        # Power up sensor peripherals.
        self.sensor_manager.power_on()

        # Ready.
        self.start_mainloop()

    def start_mainloop(self):

        # Todo: Refactor by using timers.

        # Enter the main loop.
        while True:

            # Feed the watchdog timer to keep the system alive.
            self.device.watchdog.feed()

            # Indicate activity.
            # Todo: Optionally disable this output.
            log.info('--- loop ---')

            # Run downstream mainloop handlers.
            self.loop()

            # Give the system some breath.
            machine.idle()

    def loop(self):
        """
        Main duty cycle loop.
        """

        #log.info('Terkin loop')

        # Alternative loop signalling: 1 x blue.
        # https://forum.pycom.io/topic/2067/brightness-of-on-board-led/7
        self.device.blink_led(0x00000b, count=2)

        # Read sensors.
        readings = self.read_sensors()

        # Remember current reading
        self.storage.last_reading = readings

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

        # Sleep how ever.
        self.sleep()

    def sleep(self):
        """
        Sleep until the next measurement cycle.
        """

        lightsleep = self.settings.get('main.lightsleep', False)
        deepsleep = self.settings.get('main.deepsleep', False)
        interval = self.get_sleep_time()

        # Amend deep sleep intent when masked through maintenance mode.
        if self.device.status.maintenance is True:
            lightsleep = False
            deepsleep = False
            log.info('Device is in maintenance mode. Skipping deep sleep and '
                     'adjusting interval to {} seconds'.format(interval))

        # Use deep sleep if requested.
        try:
            if deepsleep:

                # Shut down sensor peripherals.
                self.sensor_manager.power_off()

                # Shut down device peripherals.
                self.device.power_off()

            # Send device to deep sleep.
            self.device.hibernate(interval, lightsleep=lightsleep, deepsleep=deepsleep)

        # When hibernation fails, fall back to regular "time.sleep".
        except:
            log.exception('Failed to hibernate, falling back to regular sleep')
            # Todo: Emit error message here.
            log.info('Sleeping for {} seconds'.format(interval))
            time.sleep(interval)

    def get_sleep_time(self):
        interval = self.settings.get('main.interval', 60.0)

        # Configuration switchover backward compatibility / defaults.
        if isinstance(interval, (float, int)):
            self.settings.set('main.interval', {})
            self.settings.setdefault('main.interval.field', interval)
        self.settings.setdefault('main.interval.maintenance', 5.0)

        # Compute interval.
        interval = self.settings.get('main.interval.field')

        # Amend deep sleep intent when masked through maintenance mode.
        if self.device.status.maintenance is True:
            interval = self.settings.get('main.interval.maintenance')

        # FIXME
        sleep_time = interval

        return sleep_time

    def register_sensors(self):
        """
        Add system sensors.
        """

        log.info('Registering system sensors')

        system_sensors = [
            SystemMemoryFree,
            SystemTemperature,
            SystemBatteryLevel,
            SystemUptime,
        ]

        for sensor_factory in system_sensors:
            sensor = sensor_factory()
            if hasattr(sensor, 'setup') and callable(sensor.setup):
                sensor.setup(self.settings)
            self.sensor_manager.register_sensor(sensor)

        # Add WiFi metrics.
        try:
            self.sensor_manager.register_sensor(SystemWiFiMetrics(self.device.networking.wifi_manager.station))
        except:
            log.exception('Enabling SystemWiFiMetrics sensor failed')

    def read_sensors(self):
        """
        Read sensors
        """

        # Collect observations.
        data = {}
        richdata = {}

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
                    reading = sensor.read()

                # Evaluate sensor outcome.
                if reading is None or reading is AbstractSensor.SENSOR_NOT_INITIALIZED:
                    continue

                # Add sensor reading to observations.
                data.update(reading)

                # Record reading for prettified output.
                self.record_reading(sensor, reading, richdata)

            except Exception as ex:
                # Because of the ``gc_disabled`` context manager used above,
                # the propagation of exceptions has to be tweaked like that.
                log.exc(ex, 'Reading sensor "%s" failed', sensorname)

            # Feed the watchdog.
            self.device.watchdog.feed()

        # Debugging: Print sensor data before running telemetry.
        prettify_log = self.settings.get('sensors.prettify_log', False)
        if prettify_log:
            log.info('Sensor data:\n\n%s', ddformat(richdata, indent=11))
        else:
            log.info('Sensor data:  %s', data)

        return data

    def record_reading(self, sensor, reading, richdata):
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

    def transmit_readings(self, data):
        """Transmit data"""

        # TODO: Optionally disable telemetry.
        if self.device.telemetry is None:
            log.warning('Telemetry disabled')
            return False

        telemetry_status = self.device.telemetry.transmit(data)
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
