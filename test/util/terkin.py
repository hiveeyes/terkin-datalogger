# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import logging
from pyfakefs.fake_filesystem_unittest import Patcher as FakeFS


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


def invoke_umal():
    from umal import MicroPythonBootloader
    bootloader = MicroPythonBootloader()
    sys.modules['__main__'].bootloader = bootloader
    return bootloader


def invoke_datalogger_pycom(caplog, settings):
    return invoke_datalogger(caplog, settings, pycom=True)


def invoke_datalogger(caplog, settings, pycom=False):

    # Use a fake filesystem.
    with FakeFS():

        # Pycom mounts the main filesystem at "/flash".
        if pycom:
            os.mkdir('/flash')

        # Capture log output.
        with caplog.at_level(logging.DEBUG):

            # Invoke bootloader.
            bootloader = invoke_umal()

            # Invoke datalogger with a single duty cycle.
            from terkin.datalogger import TerkinDatalogger
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_cycle()

            return datalogger
