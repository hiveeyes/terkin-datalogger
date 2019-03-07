# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
"""
Convenient data logger framework conceived for the Bee Observer (BOB) project.
https://community.hiveeyes.org/c/bee-observer
"""
import settings
from hiveeyes.datalogger import HiveeyesDatalogger
from hiveeyes.sensor_hx711 import HX711Sensor


class BobDatalogger(HiveeyesDatalogger):
    """
    Yet another data logger. This time for MicroPython.
    """

    # Naming things.
    name = 'BOB MPY data logger'

    def register_sensors(self):
        """
        Add your sensors here.
        """

        # First, spin up the built-in sensors.
        super().register_sensors()

        # Add some sensors for the Bee Observer (BOB) project.
        self.device.tlog('Registering BOB sensors')

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
        # TODO: Use values from configuration settings.
        hx711_sensor = HX711Sensor(
            pin_dout='P0',
            pin_pdsck='P2',
            scale=11.026667,
            offset=130800.0,
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
        self.device.tlog('BOB loop')

        # Finally, schedule other system tasks.
        super().loop()


def main():
    """Start the data logger application."""
    datalogger = BobDatalogger(settings)
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
