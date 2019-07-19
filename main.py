# -*- coding: utf-8 -*-
#
# Ratrack MicroPython Datalogger
# https://github.com/hiveeyes/hiveeyes-micropython-firmware
#
# (c) 2019 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
"""
-----
Setup
-----

Just run::

    make setup
    make install

to bring everything into shape.

Then, invoke::

    make sketch-and-run

to upload the program and reset the ESP32.
"""

import settings
from terkin import logging
from hiveeyes.datalogger import HiveeyesDatalogger

log = logging.getLogger(__name__)


class BobDatalogger(HiveeyesDatalogger):
    """
    The Bee Observer Datalogger for MicroPython.
    """

    # Naming things.
    name = 'Bee Observer Datalogger'

    def loop(self):
        """
        Loop function. Do what I mean.
        """

        # It's your turn.
        #log.info('BOB loop')

        # Finally, schedule other system tasks.
        super().loop()


def main():
    """Start the data logger application."""
    datalogger = BobDatalogger(settings)
    datalogger.setup()
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
