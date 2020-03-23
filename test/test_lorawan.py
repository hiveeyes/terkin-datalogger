# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys
import json
import pytest
import logging
from test.util.terkin import invoke_datalogger_pycom

logger = logging.getLogger(__name__)


@pytest.mark.telemetry
@pytest.mark.lorawan
def test_system_temperature(monkeypatch, network_lora, caplog):
    """
    Pretend to invoke the datalogger on a LoPy4 with basic system sensors.
    Effectively, only the "system.temperature" sensor will be transmitted
    over LoRa telemetry.

    By intercepting the lora socket communication, proof that the
    submitted payload is correct by checking the raw payload value
    and decoding it through Cayenne.
    """

    # Define platform.
    monkeypatch.setattr(sys, 'platform', 'LoPy4')

    # Define artificial LoRa conversation.
    network_lora.register_conversation()

    # Invoke datalogger with LoRaWAN telemetry settings for a single duty cycle.
    from test.settings import telemetry_lorawan
    invoke_datalogger_pycom(caplog, settings=telemetry_lorawan)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert "Starting Terkin datalogger" in captured, captured
    assert "platform: LoPy4" in captured, captured
    assert "[LoRa] Starting LoRa Manager" in captured, captured
    assert "Telemetry transport: CayenneLPP over LoRaWAN/TTN" in captured, captured
    assert "Telemetry status: SUCCESS (1/1)" in captured, captured

    # Check the raw LoRa payload.
    from mocket import Mocket
    assert Mocket.last_request() == bytearray(b'\x00g\x01\xbf\x00\x01\x00')

    # Check the value after decoding from CayenneLPP.
    from cayennelpp import LppData
    data = LppData.from_bytes(Mocket.last_request())
    assert data.channel == 0
    assert data.type == 103
    assert data.value == (44.7,)

    assert "[LoRa] No downlink message processed" in captured, captured


@pytest.mark.telemetry
@pytest.mark.lorawan
def test_downlink_interval_set(monkeypatch, network_lora, caplog):
    """
    Simulate a downlink "set interval" command on LoRaWAN port 1.
    """

    # Define platform.
    monkeypatch.setattr(sys, 'platform', 'LoPy4')

    # Define artificial LoRa conversation.
    network_lora.register_conversation(response_port=1, response_data=[b'\x03'])

    # Invoke datalogger with LoRaWAN telemetry settings for a single duty cycle.
    from test.settings import telemetry_lorawan
    invoke_datalogger_pycom(caplog, settings=telemetry_lorawan)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert '[LoRa] Received "set deep sleep interval" command, will sleep for 3 minutes.' in captured, captured


@pytest.mark.telemetry
@pytest.mark.lorawan
def test_downlink_interval_reset(monkeypatch, network_lora, caplog):
    """
    Simulate a downlink "reset interval" command on LoRaWAN port 1.
    """

    # Define platform.
    monkeypatch.setattr(sys, 'platform', 'LoPy4')

    # Define artificial LoRa conversation.
    network_lora.register_conversation(response_port=1, response_data=[b'\x00'])

    # Invoke datalogger with LoRaWAN telemetry settings for a single duty cycle.
    from test.settings import telemetry_lorawan
    invoke_datalogger_pycom(caplog, settings=telemetry_lorawan)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert '[LoRa] Received "reset deep sleep interval" command, erasing from NVRAM.' in captured, captured


@pytest.mark.telemetry
@pytest.mark.lorawan
def test_downlink_pause(monkeypatch, network_lora, caplog):
    """
    Simulate a downlink "pause" command on LoRaWAN port 2.
    """

    # Define platform.
    monkeypatch.setattr(sys, 'platform', 'LoPy4')

    # Define artificial LoRa conversation.
    network_lora.register_conversation(response_port=2, response_data=[b'\x01'])

    # Invoke datalogger with LoRaWAN telemetry settings for a single duty cycle.
    from test.settings import telemetry_lorawan
    invoke_datalogger_pycom(caplog, settings=telemetry_lorawan)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert '[LoRa] Received "pause payload submission" command: True' in captured, captured


@pytest.mark.telemetry
@pytest.mark.lorawan
def test_downlink_unpause(monkeypatch, network_lora, caplog):
    """
    Simulate a downlink "unpause" command on LoRaWAN port 2.
    """

    # Define platform.
    monkeypatch.setattr(sys, 'platform', 'LoPy4')

    # Define artificial LoRa conversation.
    network_lora.register_conversation(response_port=2, response_data=[b'\x00'])

    # Invoke datalogger with LoRaWAN telemetry settings for a single duty cycle.
    from test.settings import telemetry_lorawan
    invoke_datalogger_pycom(caplog, settings=telemetry_lorawan)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert '[LoRa] Received "pause payload submission" command: False' in captured, captured
