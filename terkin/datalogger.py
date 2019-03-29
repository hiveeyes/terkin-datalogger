# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import utime
import machine

from terkin import __version__
from terkin.configuration import TerkinConfiguration
from terkin.device import TerkinDevice
from terkin.sensor import MemoryFree, SensorManager
from terkin.sensor import OneWireBus, I2CBus

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

    def start(self):

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
        print("INFO: starting all busses: {}".format(bus_settings))
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
                print("WARNING: invalid bus definition: {}".format(bus))

    def register_sensors(self):
        """
        Add baseline sensors.

        TODO: Add more sensors.
        - Metadata from NetworkManager.station
        - Device stats, see Microhomie
        """

        self.device.tlog('Registering Terkin sensors')

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
            print('--- loop ---')

            # Run downstream mainloop handlers.
            self.loop()

            # Yup.
            machine.idle()

    def read_sensors(self):
        """Read sensors"""
        data = {}
        for sensor in self.sensor_manager.sensors:
            sensor_name = sensor.__class__.__name__
            print('INFO:  Reading sensor "{}"'.format(sensor_name))
            try:
                reading = sensor.read()
                if reading is not None:
                    data.update(reading)
            except Exception as ex:
                print('ERROR: Reading sensor "{}" failed: {}'.format(sensor_name, ex))
                #raise

        return data

    def transmit_readings(self, data):
        """Transmit data"""

        # TODO: Optionally disable telemetry.
        if self.device.telemetry is None:
            print('WARNING: Telemetry disabled')
            return False

        success = self.device.telemetry.transmit(data)

        # Evaluate outcome.
        if success:
            self.device.tlog('Telemetry transmission: SUCCESS')
        else:
            self.device.tlog('Telemetry transmission: FAILURE')

        return success

    def loop(self):
        self.device.tlog('Terkin loop')

        # Read sensors.
        data = self.read_sensors()

        # Debugging: Print sensor data before running telemetry.
        #print(data)

        # Transmit data.
        self.transmit_readings(data)

        # Run the garbage collector.
        self.device.run_gc()

        # Sleep until the next measurement cycle.
        # TODO: Account for deep sleep here.
        utime.sleep(self.settings.get('main.interval'))
