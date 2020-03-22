import os
# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys
import json
import pytest
import logging

from pyfakefs.fake_filesystem_unittest import Patcher as FakeFS

from test.util.terkin import start_umal

logger = logging.getLogger(__name__)


if 'Microsoft' in os.uname().release:
    pytest.skip("Skipping this test on Windows/WSL", allow_module_level=True)


@pytest.mark.esp32
@pytest.mark.mqtt
@pytest.mark.telemetry
@pytest.mark.docker
def test_telemetry_mqtt(monkeypatch, caplog, mosquitto, capmqtt):

    # Define platform and start bootloader.
    monkeypatch.setattr(sys, 'platform', 'esp32')
    bootloader = start_umal()

    # Use very basic settings without networking.
    import test.settings.telemetry_mqtt as settings

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

            assert "Reading 4 sensor ports" in captured, captured
            #assert "Sensor data:  {}" in captured, captured

            assert "MQTT topic:   mqttkit-1/testdrive/area-42/node-01/data.json" in captured, captured
            assert 'MQTT payload: {"system.memfree": 1000000, "system.temperature": 44.7053182608696' in captured, captured
            assert "Telemetry status: SUCCESS (1/1)" in captured, captured

            data_reference = {
                "system.memfree": 1000000,
                "system.temperature": 44.7053182608696,
                "system.wifi.rssi": -85.3,
            }

            message_1 = capmqtt.buffer()[0]
            data_1 = json.loads(message_1)
            del data_1['system.time']
            del data_1['system.uptime']
            del data_1['system.runtime']
            assert data_1 == data_reference, capmqtt.buffer()
