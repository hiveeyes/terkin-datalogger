# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys


def monkeypatch_terkin():

    # Adjust logging module.
    import logging
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)-15s [%(name)-36s] %(levelname)-7s: %(message)s')
    import terkin.logging
    terkin.logging.getLogger = logging.getLogger

    # Override Pycom-specific chronometer.
    from terkin.util import PycomChronometer
    from umal import GenericChronometer
    import terkin.util
    terkin.util.PycomChronometer = GenericChronometer


def start_umal():
    from umal import MicroPythonBootloader
    global bootloader
    bootloader = MicroPythonBootloader()
    sys.modules['__main__'].bootloader = bootloader
    return bootloader
