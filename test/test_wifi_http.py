# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import json
import mock
import pytest

import logging
from test.util.terkin import invoke_datalogger

logger = logging.getLogger(__name__)


@pytest.mark.telemetry
@pytest.mark.http
@pytest.mark.esp32
@mock.patch('sys.platform', 'esp32')
def test_uplink_wifi_http(httpserver_ipv4, caplog):

    httpserver = httpserver_ipv4

    # Define HTTP request details.

    # Mock HTTP conversation.
    response = [
        {
            "message": "Received #1 readings",
            "type": "info"
        }
    ]
    httpserver.expect_request("/api-notls/workbench/testdrive/area-42/node-01-http-json/data").respond_with_json(response)

    # Capture HTTP request by invoking datalogger with a single duty cycle.

    import socket
    socket.setdefaulttimeout(2.0)

    # Acquire settings with HTTP telemetry.
    import test.settings.telemetry_http_json as http_settings

    # Invoke datalogger with a single duty cycle.
    datalogger = invoke_datalogger(caplog, http_settings)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert "Starting Terkin datalogger" in captured, captured
    assert "platform: esp32" in captured, captured

    assert "WiFi STA: Preparing connection to network \"FooBarWiFi\"" in captured, captured
    assert "WiFi STA: Connected to \"FooBarWiFi\"" in captured, captured
    assert "Network stack ready" in captured, captured

    assert "Reading 4 sensor ports" in captured, captured

    assert "Sending HTTP request to http://127.0.0.1:8888/api-notls/workbench/testdrive/area-42/node-01-http-json/data" in captured, captured
    assert 'HTTP payload: {"system.memfree": 1000000, "system.temperature": 44.7053182608696' in captured, captured
    assert "Telemetry status: SUCCESS (1/1)" in captured, captured

    # Proof it worked by checking the HTTP request body.
    data_reference = {
        "system.memfree": 1000000,
        "system.temperature": 44.7053182608696,
        "system.wifi.rssi": -85.3,
    }

    # Assume there has been a single HTTP conversation.
    assert len(httpserver.log) == 1, "pytest-httpserver didn't capture any request"

    # Acquire request and response from last conversation.
    request, response = httpserver.log[0]

    # Decode JSON request body and adjust data.
    data = json.loads(request.get_data())
    del data['system.time']
    del data['system.uptime']
    del data['system.runtime']

    # Check, check, check.
    assert data_reference == data, data
