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


def invoke_datalogger_pycom(caplog, settings, after_setup=None):
    return invoke_datalogger(caplog, settings, pycom=True, after_setup=after_setup)


def invoke_datalogger_raspberrypi(caplog, settings):

    import fake_rpi

    # Fake RPi
    sys.modules['RPi'] = fake_rpi.RPi

    # Fake GPIO
    sys.modules['RPi.GPIO'] = fake_rpi.RPi.GPIO

    # Fake smbus (I2C)
    sys.modules['smbus'] = fake_rpi.smbus

    return invoke_datalogger(caplog, settings, raspberrypi=True)


def invoke_datalogger(caplog, settings, pycom=False, raspberrypi=False, after_setup=None):

    # Use a fake filesystem.
    with FakeFS(additional_skip_names=["serial", "serial.serialutil", "serial.serialposix"]):

        # Pycom mounts the main filesystem at "/flash".
        if pycom:
            os.mkdir('/flash')

        if raspberrypi:
            os.makedirs('/sys/firmware/devicetree/base')
            with open('/sys/firmware/devicetree/base/model', 'w') as f:
                f.write('Raspberry')

            os.makedirs('/sys/bus/w1/devices/w1_bus_master1')
            with open('/sys/bus/w1/devices/w1_bus_master1/w1_master_slaves', 'w') as f:
                f.writelines(['28-ff641d8fdf18c1\n', '28-ff641d8fc3944f\n'])

            os.makedirs('/sys/bus/w1/devices/w1_bus_master1/28-ff641d8fdf18c1')
            with open('/sys/bus/w1/devices/w1_bus_master1/28-ff641d8fdf18c1/w1_slave', 'w') as f:
                f.write('YES\nt=48187')

            os.makedirs('/sys/bus/w1/devices/w1_bus_master1/28-ff641d8fc3944f')
            with open('/sys/bus/w1/devices/w1_bus_master1/28-ff641d8fc3944f/w1_slave', 'w') as f:
                f.write('YES\nt=48187')

            os.makedirs('/dev')
            with open('/dev/i2c-3', 'w') as f:
                f.write('nonsense')

        # Capture log output.
        with caplog.at_level(logging.DEBUG):

            # Invoke bootloader.
            bootloader = invoke_umal()

            # Invoke datalogger with a single duty cycle.
            from terkin.datalogger import TerkinDatalogger
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()

            if callable(after_setup):
                after_setup(datalogger=datalogger)

            datalogger.duty_cycle()

            return datalogger
