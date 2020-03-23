# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys

import mock
import pytest
import logging

from pyfakefs.fake_filesystem_unittest import Patcher as FakeFS

from test.util.terkin import invoke_umal


@pytest.mark.basic
@pytest.mark.esp32
@mock.patch('sys.platform', 'esp32')
def test_basic_esp32(caplog):

    # Use very basic settings without networking.
    import test.settings.basic as settings

    with FakeFS():

        with caplog.at_level(logging.DEBUG):

            # Invoke bootloader.
            bootloader = invoke_umal()

            # Start datalogger with a single duty cycle on a fake filesystem.
            from terkin.datalogger import TerkinDatalogger
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_task()

            # Capture log output.
            captured = caplog.text

            # Proof it works by verifying log output.
            assert "Starting Terkin datalogger" in captured, captured
            assert "platform: esp32" in captured, captured
            assert "[WiFi] interface disabled in settings" in captured, captured
            assert "[LoRa] This is not a LoRa capable device" in captured, captured
            assert "[GPRS] Interface disabled in settings" in captured, captured
            assert "Reading 0 sensor ports" in captured, captured
            assert "Sensor data:  {}" in captured, captured
            assert "Telemetry status: SUCCESS (0/0)" in captured, captured


@pytest.mark.basic
@pytest.mark.pycom
@pytest.mark.wipy
@mock.patch('sys.platform', 'WiPy')
def test_basic_wipy(caplog):

    # Use very basic settings without networking.
    import test.settings.basic as settings

    with FakeFS():
        # Pycom mounts the main filesystem at "/flash".
        os.mkdir('/flash')

        with caplog.at_level(logging.DEBUG):

            # Invoke bootloader.
            bootloader = invoke_umal()

            # Start datalogger with a single duty cycle on a fake filesystem.
            from terkin.datalogger import TerkinDatalogger
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_task()

            # Capture log output.
            captured = caplog.text

            # Proof it works by verifying log output.
            assert "Starting Terkin datalogger" in captured, captured
            assert "platform: WiPy" in captured, captured


@pytest.mark.basic
@pytest.mark.cpython
@mock.patch('sys.platform', 'linux2')
def test_basic_cpython(caplog):

    # Use very basic settings without networking.
    import test.settings.basic as settings

    with FakeFS():

        with caplog.at_level(logging.DEBUG):

            # Invoke bootloader.
            bootloader = invoke_umal()

            # Start datalogger with a single duty cycle on a fake filesystem.
            from terkin.datalogger import TerkinDatalogger
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_task()

            # Capture log output.
            captured = caplog.text

            # Proof it works by verifying log output.
            assert "Starting Terkin datalogger" in captured, captured
            assert "platform: linux2" in captured, captured
