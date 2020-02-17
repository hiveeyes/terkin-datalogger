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
from terkin.datalogger import TerkinDatalogger


class ExampleDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This time for MicroPython.
    """

    # Naming things.
    name = 'Example MicroPython Datalogger'

    def read_sensors(self):
        # Fixed CayenneLPP example

        # Payload Base64: AWf8sABnAag=
        # Payload Hex:    0167FCB0006701A8
        data = {
            'temperature_0': 42.42,
            'temperature_1': -84.84,
        }
        return data


def main():
    """Start the data logger application."""
    datalogger = ExampleDatalogger(settings)
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
