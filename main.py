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
from hiveeyes import webserver
import machine
import time

log = logging.getLogger(__name__)


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
        test_server = False
        # It's your turn.
        #log.info('BOB loop')

        # Finally, schedule other system tasks.

        if (machine.reset_cause() != 0 and not test_server):
            super().loop()
        else:
            log.info('enabled AP')
            # todo: open access-point
            # for now: start webserver
            if not webserver.mws.IsStarted():
                webserver.mws.Start(threaded=True)
                log.info('You have 10 minutes until AP-mode is disabled automatically')
                time.sleep_ms(1000*60*10)
                machine.reset()



def main():
    """Start the data logger application."""
    datalogger = BobDatalogger(settings)
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
