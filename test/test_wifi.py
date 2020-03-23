# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import pytest
import logging

from pyfakefs.fake_filesystem_unittest import Patcher as FakeFS

from test.util.terkin import invoke_umal


@pytest.mark.esp32
def test_wifi_esp32(monkeypatch, caplog):

    # Define platform and start bootloader.
    monkeypatch.setattr(sys, 'platform', 'esp32')
    bootloader = invoke_umal()

    # Use very basic settings without networking.
    import test.settings.wifi as settings

    # Start datalogger with a single duty cycle on a fake filesystem.
    from terkin.datalogger import TerkinDatalogger
    with FakeFS():

        with caplog.at_level(logging.DEBUG):
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

            assert "[LoRa] This is not a LoRa capable device" in captured, captured
            assert "[GPRS] Interface disabled in settings" in captured, captured
            assert "Reading 0 sensor ports" in captured, captured
            assert "Sensor data:  {}" in captured, captured
            assert "Telemetry status: SUCCESS (0/0)" in captured, captured


@pytest.mark.pycom
@pytest.mark.wipy
def test_wifi_wipy(monkeypatch, caplog):

    # Define platform and start bootloader.
    monkeypatch.setattr(sys, 'platform', 'WiPy')
    bootloader = invoke_umal()

    # Use very basic settings without networking.
    import test.settings.wifi as settings

    # Start datalogger with a single duty cycle on a fake filesystem.
    from terkin.datalogger import TerkinDatalogger
    with FakeFS():

        # Pycom mounts the main filesystem at "/flash".
        os.mkdir('/flash')

        with caplog.at_level(logging.DEBUG):
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_task()

            # Capture log output.
            captured = caplog.text

            # Proof it works by verifying log output.
            assert "Starting Terkin datalogger" in captured, captured
            assert "platform: WiPy" in captured, captured

            assert "WiFi STA: Preparing connection to network \"FooBarWiFi\"" in captured, captured
            assert "WiFi STA: Connected to \"FooBarWiFi\"" in captured, captured
            assert "Network stack ready" in captured, captured


@pytest.mark.cpython
def test_wifi_cpython(monkeypatch, caplog):

    # Define platform and start bootloader.
    monkeypatch.setattr(sys, 'platform', 'linux2')
    bootloader = invoke_umal()

    # Use very basic settings without networking.
    import test.settings.wifi as settings

    # Start datalogger with a single duty cycle on a fake filesystem.
    from terkin.datalogger import TerkinDatalogger
    with FakeFS():

        with caplog.at_level(logging.DEBUG):
            datalogger = TerkinDatalogger(settings, platform_info=bootloader.platform_info)
            datalogger.setup()
            datalogger.duty_task()

            # Capture log output.
            captured = caplog.text

            # Proof it works by verifying log output.
            assert "Starting Terkin datalogger" in captured, captured
            assert "platform: linux2" in captured, captured

            assert "WiFi STA: Preparing connection to network \"FooBarWiFi\"" in captured, captured
            assert "WiFi STA: Connected to \"FooBarWiFi\"" in captured, captured
            assert "Network stack ready" in captured, captured
