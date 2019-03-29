# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import utime
import machine

from terkin import __version__, logging
from terkin.configuration import TerkinConfiguration
from terkin.device import TerkinDevice
from terkin.sensor import MemoryFree, SensorManager, AbstractSensor
from terkin.sensor import OneWireBus, I2CBus

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
        self.device = None
        self.sensor_manager = SensorManager()

    @property
    def appname(self):
        return '{} {}'.format(self.name, self.version)

    def start(self):

        log.info('Starting %s', self.appname)

        # Main application object.
        self.device = TerkinDevice(name=self.name, version=self.version, settings=self.settings)

        # Disable this if you don't want serial access.
        #self.device.enable_serial()

        # Hello world.
        self.device.print_bootscreen()

        # Bootstrap infrastructure.
        self.device.start_networking()
        self.device.start_telemetry()

        # Signal readyness by publishing information about the device (Microhomie).
        # self.device.publish_properties()

        self.register_busses()
        self.register_sensors()

        self.start_mainloop()

    def register_busses(self):
        bus_settings = self.settings.get('sensors.busses')
        log.info("Starting all busses %s", bus_settings)
        for bus in bus_settings:
            if not bus.get("enabled", False):
                continue
            if bus['family'] == 'onewire':
                owb = OneWireBus(bus["number"])
                owb.register_pin("data", bus['pin_data'])
                owb.start()
                name = bus["family"] + ":" + str(bus["number"])
                self.sensor_manager.register_bus(name, owb)

            elif bus['family'] == 'i2c':
                i2c = I2CBus(bus["number"])
                i2c.register_pin("sda", bus['pin_sda'])
                i2c.register_pin("scl", bus['pin_scl'])
                i2c.start()
                name = bus["family"] + ":" + str(bus["number"])
                self.sensor_manager.register_bus(name, i2c)

            else:
                log.warning("Invalid bus configuration: %s", bus)

    def register_sensors(self):
        """
        Add baseline sensors.

        TODO: Add more sensors.
        - Metadata from NetworkManager.station
        - Device stats, see Microhomie
        """

        log.info('Registering Terkin sensors')

        memfree = MemoryFree()
        self.sensor_manager.register_sensor(memfree)

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

    def read_sensors(self):
        """Read sensors"""
        data = {}
        for sensor in self.sensor_manager.sensors:

            sensor_name = sensor.__class__.__name__
            log.info('Reading sensor "%s"', sensor_name)

            try:
                reading = sensor.read()
                if reading is None or reading is AbstractSensor.SENSOR_NOT_INITIALIZED:
                    continue
                data.update(reading)

            except:
                log.exception('Reading sensor "%s" failed', sensor_name)

        return data

    def transmit_readings(self, data):
        """Transmit data"""

        # TODO: Optionally disable telemetry.
        if self.device.telemetry is None:
            log.warning('Telemetry disabled')
            return False

        success = self.device.telemetry.transmit(data)

        # Evaluate outcome.
        if success:
            log.info('Telemetry transmission: SUCCESS')
        else:
            log.info('Telemetry transmission: FAILURE')

        return success

    def loop(self):
        log.info('Terkin loop')

        # Read sensors.
        data = self.read_sensors()

        # Debugging: Print sensor data before running telemetry.
        #log.debug(data)

        # Transmit data.
        self.transmit_readings(data)

        # Run the garbage collector.
        self.device.run_gc()

        # Sleep until the next measurement cycle.
        # TODO: Account for deep sleep here.
        utime.sleep(self.settings.get('main.interval'))
