# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import pytest

from test.util.terkin import invoke_umal


@pytest.mark.basic
@pytest.mark.esp32
def test_basic_esp32(mocker, caplog):

    # Define platform.
    mocker.patch("sys.platform", "esp32")

    # Use very basic settings without networking.
    import test.settings.basic as settings

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
    assert "[WiFi] Interface not enabled in settings." in captured, captured
    assert "[LoRa] Interface not enabled in settings." in captured, captured
    assert "[GPRS] Interface not enabled in settings." in captured, captured
    assert "Reading 0 sensor ports" in captured, captured
    assert "Sensor data:  {}" in captured, captured
    assert "Telemetry status: SUCCESS (0/0)" in captured, captured


@pytest.mark.basic
@pytest.mark.pycom
@pytest.mark.wipy
def test_basic_wipy(mocker, fs_no_root, caplog):

    # Define platform.
    mocker.patch("sys.platform", "WiPy")

    # Use very basic settings without networking.
    import test.settings.basic as settings

    # Pycom mounts the main filesystem at "/flash".
    os.mkdir('/flash')

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
def test_basic_cpython(mocker, caplog):

    # Define platform.
    mocker.patch("sys.platform", "linux2")

    # Use very basic settings without networking.
    import test.settings.basic as settings

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
