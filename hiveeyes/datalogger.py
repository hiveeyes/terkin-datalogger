# -*- coding: utf-8 -*-
#
# Hiveeyes MicroPython Datalogger
# https://github.com/hiveeyes/hiveeyes-micropython-firmware
#
# Conceived for the Bee Observer (BOB) project.
# https://community.hiveeyes.org/c/bee-observer
#
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
from terkin.datalogger import TerkinDatalogger
from hiveeyes.sensor_hx711 import HX711Sensor
from hiveeyes.sensor_ds18x20 import DS18X20Sensor
from terkin.sensor import OneWireBus


class HiveeyesDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This time for MicroPython.
    """

    # Naming things.
    name = 'Hiveeyes MicroPython Datalogger'

    def register_sensors(self):
        """
        Add your sensors here.
        """

        # First, spin up the built-in sensors.
        super().register_sensors()

        # Add some sensors for the Hiveeyes project.
        self.device.tlog('Registering Hiveeyes sensors')

        ds18x20_settings = self.settings.get('sensors.registry.ds18x20')
        owb = OneWireBus()
        owb.register_pin("data", ds18x20_settings['pin_data'])
        owb.start()

        self.register_bus("onewire:0", owb)

        # Setup the HX711.
        try:
            self.add_hx711_sensor()
        except Exception as ex:
            print('INFO:  Skipping HX711 sensor. {}'.format(ex))
            raise

        # Setup the HX711.
        try:
            self.add_ds18x20_sensor()
        except Exception as ex:
            print('INFO:  Skipping DS18x20 sensor. {}'.format(ex))
            raise

    def add_hx711_sensor(self):
        """
        Setup and register the HX711 sensor component with your data logger.
        """

        # Initialize HX711 sensor component.
        hx711_settings = self.settings.get('sensors.registry.hx711')

        hx711_sensor = HX711Sensor()
        hx711_sensor.register_pin('dout', hx711_settings['pin_dout'])
        hx711_sensor.register_pin('dsck', hx711_settings['pin_dout'])
        hx711_sensor.register_parameter('scale', hx711_settings['scale'])
        hx711_sensor.register_parameter('offset', hx711_settings['offset'])
        hx711_sensor.register_parameter('gain', hx711_settings.get('gain', 128))
        hx711_sensor.select_driver('heisenberg')

        # Select driver module. Use "gerber" (vanilla) or "heisenberg" (extended).

        # Start sensor.
        hx711_sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(hx711_sensor)


    def add_ds18x20_sensor(self):
        """
        Setup and register the DS18X20  sensor component with your data logger.
        """

        bus = self.sensor_manager.get_bus_by_name('onewire:0')
        ds18x20_sensor = DS18X20Sensor()
        ds18x20_sensor.acquire_bus(bus)


        # Select driver module. Use "gerber" (vanilla) or "heisenberg" (extended).

        # Start sensor.
        ds18x20_sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(ds18x20_sensor)



    def loop(self):
        """
        Loop function. Do what I mean.
        """

        # It's your turn.
        #self.device.tlog('Hiveeyes loop')

        # Finally, schedule other system tasks.
        super().loop()
