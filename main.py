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
import settings
from hiveeyes.datalogger import HiveeyesDatalogger


class BobDatalogger(HiveeyesDatalogger):
    """
    The BOB MicroPython Datalogger.
    """

    # Naming things.
    name = 'BOB MicroPython Datalogger'

    def loop(self):
        """
        Loop function. Do what I mean.
        """

        # It's your turn.
        #self.device.tlog('BOB loop')

        # Finally, schedule other system tasks.
        super().loop()


def main():
    """Start the data logger application."""
    datalogger = BobDatalogger(settings)
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
