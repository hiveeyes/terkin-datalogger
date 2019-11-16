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

    print('[main.py] INFO: Loading Terkin Datalogger')
    global bootloader
    global datalogger

    print('[main.py] INFO: Loading modules')
    from terkin.datalogger import TerkinDatalogger

    datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
    datalogger.setup()

    try:
        datalogger.start()

    except KeyboardInterrupt:
        log.info("Received KeyboardInterrupt within main thread")

        if datalogger.device.networking is not None:
            datalogger.device.networking.stop_modeserver()
            datalogger.device.networking.wifi_manager.stop()

            # This helps the webserver to get rid of any listening sockets.
            # https://github.com/jczic/MicroWebSrv2/issues/8
            datalogger.device.networking.stop_httpserver()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
