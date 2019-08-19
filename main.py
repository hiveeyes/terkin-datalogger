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
Please check https://community.hiveeyes.org/t/operate-the-terkin-datalogger-sandbox/2332
in order to get an idea how to operate this software sandbox.

Have fun!
"""

print('[main.py] INFO: Loading settings')
import settings

print('[main.py] INFO: Starting logging')
from terkin import logging
log = logging.getLogger(__name__)


# Global reference to Datalogger object.
datalogger = None


def main():
    """Start the data logger application."""
    print('[main.py] INFO: Starting Terkin Datalogger')
    global bootloader
    global datalogger
    print('[main.py] INFO: Loading modules')
    from hiveeyes.datalogger import HiveeyesDatalogger
    datalogger = HiveeyesDatalogger(settings, platform_info=bootloader.platform_info)
    datalogger.setup()
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
