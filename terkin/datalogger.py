# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import machine

from terkin import __version__, logging
from terkin.configuration import TerkinConfiguration
from terkin.device import TerkinDevice
from terkin.radio import SystemWiFiMetrics
from terkin.sensor import SensorManager, AbstractSensor
from terkin.sensor.system import SystemMemoryFree, SystemTemperature, SystemBatteryLevel, SystemUptime

log = logging.getLogger(__name__)


# Maybe refactor to TerkinCore.
class TerkinDatalogger:

    # Application metadata.
    name = 'Terkin MicroPython Datalogger'
    version = __version__

    def __init__(self, settings):
        self.settings = TerkinConfiguration()
        self.settings.add(settings)
        self.settings.dump()

        self.sensor_manager = SensorManager()
        self.device = TerkinDevice(name=self.name, version=self.version, settings=self.settings)

    @property
    def appname(self):
        return '{} {}'.format(self.name, self.version)

    def start(self):

        log.info('Starting %s', self.appname)

        # Report about wakeup reason and run wakeup tasks.
        self.device.resume()

        # Disable this if you don't want serial access.
        #self.device.enable_serial()

        # Hello world.
        self.device.print_bootscreen()

        # Bootstrap infrastructure.
        self.device.start_networking()

        # Conditionally start telemetry if networking is available.
        if self.device.status.networking:
            self.device.start_telemetry()

        # Signal readyness by publishing information about the device (Microhomie).
        # self.device.publish_properties()

        bus_settings = self.settings.get('sensors.busses')
        self.sensor_manager.register_busses(bus_settings)
        self.register_sensors()

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
            # TODO: Optionally disable this output.
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

        # Create sensor adapters.
        for sensor_factory in system_sensors:
            sensor = sensor_factory()
            if hasattr(sensor, 'setup') and callable(sensor.setup):
                sensor.setup(self.settings)
            self.sensor_manager.register_sensor(sensor)

        # Add WiFi metadata.
        self.sensor_manager.register_sensor(SystemWiFiMetrics(self.device.networking.station))

    def read_sensors(self):
        """Read sensors"""
        data = {}
        sensors = self.sensor_manager.sensors
        log.info('Reading %s sensor ports', len(sensors))
        for sensor in sensors:

            sensor_name = sensor.__class__.__name__
            log.debug('Reading sensor "%s"', sensor_name)

            try:
                reading = sensor.read()
                if reading is None or reading is AbstractSensor.SENSOR_NOT_INITIALIZED:
                    continue
                data.update(reading)

            except:
                log.exception('Reading sensor "%s" failed', sensor_name)

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
