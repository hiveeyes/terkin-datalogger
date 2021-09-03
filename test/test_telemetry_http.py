# -*- coding: utf-8 -*-
# (c) 2021 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import csv
import io
import logging
from test.util.terkin import invoke_datalogger

import mock
import pytest
from freezegun import freeze_time

logger = logging.getLogger(__name__)


@pytest.mark.telemetry
@pytest.mark.http
@freeze_time("2019-03-01 22:09:52")
@mock.patch('sys.platform', 'linux')
def test_telemetry_http_csv(httpserver_ipv4, caplog):
    httpserver = httpserver_ipv4

    # Define HTTP request details.

    # Mock HTTP conversation.
    response = [
        {
            "message": "Received #1 readings",
            "type": "info"
        }
    ]
    httpserver.expect_request("/foobar").respond_with_json(response)

    # Capture HTTP request by invoking datalogger with a single duty cycle.

    import socket
    socket.setdefaulttimeout(2.0)

    # Acquire settings with HTTP telemetry.
    import test.settings.telemetry_http_csv as http_settings

    # Invoke datalogger with a single duty cycle.
    datalogger = invoke_datalogger(caplog, http_settings)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert "Starting Terkin datalogger" in captured, captured
    assert "platform: linux" in captured, captured

    assert "Reading 3 sensor ports" in captured, captured

    assert "http://127.0.0.1:8888/foobar" in captured, captured
    assert "Telemetry status: SUCCESS (1/1)" in captured, captured

    # Proof it worked by checking the HTTP request body.
    data_reference = {
        "datetime.ISO8601": "2019-03-01T22:09:52",
        "system.memfree": "1000000",
        "system.temperature": "44.7053182608696",
        "system.time": "1551478192.0",
        "system.uptime": "1551478192.0",
    }

    # Assume there has been a single HTTP conversation.
    assert len(httpserver.log) == 1, "pytest-httpserver didn't capture any request"

    # Acquire request and response from last conversation.
    request, response = httpserver.log[0]

    # Converge request payload into string buffer.
    payload = request.get_data().decode()
    buffer = io.StringIO(payload)

    # Decode CSV.
    reader = csv.DictReader(buffer)

    # Read first data row.
    data = next(reader)

    # This field is not deterministic, so skip it from comparison.
    del data['system.runtime']

    # Check, check, check.
    assert data_reference == data, data
