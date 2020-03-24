# -*- coding: utf-8 -*-
#
# Terkin Datalogger
# https://github.com/hiveeyes/terkin-datalogger
#
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
import settings
from terkin import logging
from terkin.datalogger import TerkinDatalogger

log = logging.getLogger(__name__)


class DummySensor:

    def read(self):
        # Fake measurement.
        data = {"temperature": 42.84, "humidity": 83}
        return data


class ExampleDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This is for MicroPython.
    """

    # Naming things.
    name = 'Example MicroPython Datalogger'

    def register_sensors(self):
        """
        Add your sensors here.
        """

        # First, spin up the built-in sensors.
        super().register_sensors()

        # Add some sensors.
        log.info('Registering custom sensors')

        # Add a new sensor. This is just an example sensor.
        sensor = DummySensor()
        self.sensor_manager.register_sensor(sensor)


def main():
    """Start the data logger application."""
    datalogger = ExampleDatalogger(settings)
    datalogger.setup()
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
