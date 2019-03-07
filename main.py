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


class BobDatalogger(HiveeyesDatalogger):
    """
    Yet another data logger. This is for MicroPython.
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


    def loop(self):
        """
        Loop function. Do what I mean.
        """

        # It's your turn.
        print()
        self.device.tlog('BOB loop')

        # Finally, schedule all system tasks.
        super().loop()


def main():
    """Start the data logger application."""
    datalogger = BobDatalogger(settings)
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
