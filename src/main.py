# -*- coding: utf-8 -*-
#
# Terkin Datalogger
# https://github.com/hiveeyes/terkin-datalogger
#
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019-2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
#
# License: GNU Affero General Public License, Version 3
#
# Documentation: https://terkin.org
#
# Have fun!

print('[main.py] INFO: Loading settings')
try:
    import settings
except ImportError:
    print('[main.py] INFO: No python settings detected')
    settings = None

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

    # Setup datalogger.
    datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
    datalogger.setup()

    # Invoke datalogger.
    try:
        datalogger.start()

    except KeyboardInterrupt:
        log.info("Received KeyboardInterrupt")

        # Shut down networking.
        #if datalogger.device.networking is not None:
        #    datalogger.device.networking.stop()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()

    """
    from terkin.ui import TerkinUi

    ui = TerkinUi()
    try:
        ui.start()
        ui.example()

    finally:
        ui.stop()
    """
