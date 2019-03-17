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

        # Setup the HX711.
        try:
            self.add_hx711_sensor()
        except Exception as ex:
            print('INFO:  Skipping HX711 sensor. {}'.format(ex))

    def add_hx711_sensor(self):
        """
        Setup and register the HX711 sensor component with your data logger.
        """

        # Initialize HX711 sensor component.
        hx711_settings = self.settings.get('sensors.registry.hx711')

        hx711_sensor = HX711Sensor(
            pin_dout=hx711_settings['pin_dout'],
            pin_pdsck=hx711_settings['pin_pdsck'],
            scale=hx711_settings['scale'],
            offset=hx711_settings['offset'],
        )

        # Select driver module. Use "gerber" (vanilla) or "heisenberg" (extended).
        hx711_sensor.select_driver('heisenberg')

        # Start sensor.
        hx711_sensor.start()

        # Register with framework.
        self.register_sensor(hx711_sensor)

    def loop(self):
        """
        Loop function. Do what I mean.
        """

        # It's your turn.
        #self.device.tlog('Hiveeyes loop')

        # Finally, schedule other system tasks.
        super().loop()
