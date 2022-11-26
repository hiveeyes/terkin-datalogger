# -*- coding: utf-8 -*-
# (c) 2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import pytest
import logging

from test.util.terkin import invoke_umal


@pytest.mark.basic
@pytest.mark.esp32
def test_rtc_ntp_success(mocker, caplog):

    # Define platform.
    mocker.patch("sys.platform", "esp32")

    # Use very basic settings without networking.
    import test.settings.rtc_ntp as settings

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

    assert "WiFi STA: Preparing connection to network \"FooBarWiFi\"" in captured, captured
    assert "WiFi STA: Connected to \"FooBarWiFi\"" in captured, captured
    assert "Network stack ready" in captured, captured

    assert "Syncing RTC with NTP server \"pool.example.org\"" in captured, captured

    assert "Reading 0 sensor ports" in captured, captured
    assert "Sensor data:  {}" in captured, captured
    assert "Telemetry status: SUCCESS (0/0)" in captured, captured

    datalogger.device.rtc.ntp_sync.assert_called_once_with("pool.example.org", 360)
    datalogger.device.rtc.now.assert_called()
