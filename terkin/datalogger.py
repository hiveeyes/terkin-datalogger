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
from terkin.sensor.button import ButtonManager

log = logging.getLogger(__name__)


# Maybe refactor to TerkinCore.
class TerkinDatalogger:

    # Application metadata.
    name = 'Terkin MicroPython Datalogger'
    version = __version__

    def __init__(self, settings):

        # Obtain configuration settings.
        self.settings = TerkinConfiguration()
        self.settings.add(settings)

        # Button manager instance (optional).
        self.button_manager = None

        # Initialize sensor domain.
        self.sensor_manager = SensorManager()

        # Initialize device.
        self.device = TerkinDevice(name=self.name, version=self.version, settings=self.settings)

    @property
    def appname(self):
        return '{} {}'.format(self.name, self.version)

    def start(self):

        # Report about wakeup reason and run wakeup tasks.
        self.device.resume()

        # Turn off LTE modem and Bluetooth as we don't use them yet.
        # Todo: Revisit where this should actually go.
        self.device.power_off_lte_modem()
        self.device.power_off_bluetooth()

        log.info('Starting %s', self.appname)

        # Configure RGB-LED according to settings.
        self.device.configure_rgb_led()

        logging_enabled = self.settings.get('main.logging.enabled', False)
        if not logging_enabled:
            logging.disable_logging()

        # Dump configuration settings.
        log_configuration = self.settings.get('main.logging.configuration', False)
        if log_configuration:
            self.settings.dump()

        # Initialize buttons / touch pads.
        buttons_enabled = self.settings.get('sensors.system.buttons.enabled', False)
        if buttons_enabled:
            self.button_manager = ButtonManager()
            self.start_buttons()

        # Disable this if you don't want serial access.
        #self.device.enable_serial()

        # Hello world.
        if logging_enabled:
            self.device.print_bootscreen()

        # Bootstrap infrastructure.
        self.device.start_networking()

        # Conditionally start telemetry if networking is available.
        if self.device.status.networking:
            self.device.start_telemetry()

        # Todo: Signal readyness by publishing information about the device (Microhomie).
        # e.g. ``self.device.publish_properties()``

        # Setup sensors.
        bus_settings = self.settings.get('sensors.busses')
        self.sensor_manager.register_busses(bus_settings)
        self.register_sensors()

        # Power up sensor peripherals.
        self.sensor_manager.power_on()

        # Ready.
        self.start_mainloop()

    def start_mainloop(self):
        # TODO: Refactor by using timers.

        # Start the watchdog for sanity.
        #self.device.start_wdt()

        # Enter the main loop.
        while True:

            # Feed the watchdog timer to keep the system alive.
            self.device.feed_wdt()

            # Indicate activity.
            # Todo: Optionally disable this output.
            log.info('--- loop ---')

            # Run downstream mainloop handlers.
            self.loop()

            # Yup.
            machine.idle()

    def loop(self):
        """
        Main duty cycle loop.
        """

        #log.info('Terkin loop')

        # Read sensors.
        readings = self.read_sensors()

        # Transmit data.
        self.transmit_readings(readings)

        # Run the garbage collector.
        self.device.run_gc()

        # Sleep how ever.
        self.sleep()

    def sleep(self):
        """
        Sleep until the next measurement cycle.
        """
        interval = self.settings.get('main.interval')
        #print(dir(machine))

        # Use deep sleep if requested.
        try:
            deep = self.settings.get('main.deepsleep', False)
            if deep:

                # Shut down sensor peripherals.
                self.sensor_manager.power_off()

                # Shut down device peripherals.
                self.device.power_off()

            # Send device to deep sleep.
            self.device.hibernate(interval, deep=deep)

        # When hibernation fails, fall back to regular "time.sleep".
        except:
            log.exception('Failed to hibernate, falling back to regular sleep')
            # Todo: Emit error message here.
            log.info('Sleeping for {} seconds'.format(interval))
            time.sleep(interval)

    def register_sensors(self):
        """
        Add system sensors.
        """

        log.info('Registering Terkin sensors')

        system_sensors = [
            SystemMemoryFree,
            SystemTemperature,
            SystemBatteryLevel,
            SystemUptime,
        ]

        # Create environmental sensor adapters.
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
        """Read sensors"""
        data = {}
        sensors = self.sensor_manager.sensors
        log.info('Reading %s sensor ports', len(sensors))
        for sensor in sensors:

            sensorname = sensor.__class__.__name__
            log.info('Reading sensor port "%s"', sensorname)

            try:
                reading = sensor.read()
                if reading is None or reading is AbstractSensor.SENSOR_NOT_INITIALIZED:
                    continue
                data.update(reading)

            except:
                log.exception('Reading sensor "%s" failed', sensorname)

        # Debugging: Print sensor data before running telemetry.
        log.info('Sensor data:  %s', data)

        return data

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

        # Will yield ``ValueError: Touch pad error``.
        #self.button_manager.setup_touchpad('P20', name='Touch8', location='Module-Right-Top-7th')
        #self.button_manager.setup_touchpad('P19', name='Touch9', location='Module-Right-Top-8th')
