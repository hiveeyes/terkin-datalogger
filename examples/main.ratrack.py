# -*- coding: utf-8 -*-
#
# Ratrack MicroPython Datalogger
# https://github.com/hiveeyes/terkin-datalogger
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
from ratrack.datalogger import RatrackDatalogger


def main():
    """Start the data logger application."""
    datalogger = RatrackDatalogger(settings)
    datalogger.setup()
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
