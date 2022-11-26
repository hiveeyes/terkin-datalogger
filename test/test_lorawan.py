# -*- coding: utf-8 -*-
# (c) 2019-2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2019-2020 Matthias Büchner <https://github.com/thiasB>
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
"""
About
=====
Invoke the datalogger program replaying different LoRaWAN
communication scenarios and testing for their outcomes.

Setup
=====
- https://github.com/hiveeyes/terkin-datalogger/blob/main/doc/tests.rst

Synopsis
========
To invoke these tests, just type::

    make test marker="lorawan"

"""
import pytest
import logging
from test.util.terkin import invoke_datalogger_pycom

logger = logging.getLogger(__name__)


@pytest.mark.telemetry
@pytest.mark.lorawan
def test_uplink_system_temperature(mocker, network_lora, caplog):
    """
    Pretend to invoke the datalogger on a LoPy4 with basic system sensors.
    Effectively, only the "system.temperature" sensor will be transmitted
    over LoRa telemetry.

    By intercepting the lora socket communication, proof that the
    submitted payload is correct by checking the raw payload value
    and decoding it through Cayenne.
    """

    # Define platform and start bootloader.
    mocker.patch("sys.platform", "LoPy4")

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
    assert "[LoRa] Starting LoRa Adapter" in captured, captured
    assert "Telemetry transport: CayenneLPP over LoRaWAN/TTN" in captured, captured
    assert "Telemetry status: SUCCESS (1/1)" in captured, captured

    # Check the raw LoRa payload.
    from mocket import Mocket
    assert Mocket.last_request() == bytearray(b'\x00g\x01\xbf\x00\x01\x00')

    # Check the value after decoding from CayenneLPP.
    from cayennelpp import LppFrame
    data = LppFrame.from_bytes(Mocket.last_request()).data

    # System temperature
    assert data[0].channel == 0
    assert data[0].type == 103
    assert data[0].value == (44.7,)

    # EOF?
    assert data[1].channel == 0
    assert data[1].type == 1
    assert data[1].value == (0,)

    assert "[LoRa] No downlink message processed" in captured, captured


@pytest.mark.telemetry
@pytest.mark.lorawan
def test_uplink_environmental_sensors(mocker, network_lora, caplog):
    """
    Pretend to invoke the datalogger on a LoPy4 with environmental sensors.

    By intercepting the lora socket communication, proof that the
    submitted payload is correct by checking the raw payload value
    and decoding it through Cayenne.
    """

    mocker.patch("sys.platform", "LoPy4")

    # Define artificial LoRa conversation.
    network_lora.register_conversation()

    # Mix together different settings.
    from test.settings import telemetry_lorawan
    from test.settings import sensors_micropython as sensor_settings
    mocker.patch('test.settings.telemetry_lorawan.sensors', sensor_settings.sensors)

    # Invoke datalogger with LoRaWAN telemetry settings for a single duty cycle.
    invoke_datalogger_pycom(caplog, settings=telemetry_lorawan)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert "Starting Terkin datalogger" in captured, captured
    assert "platform: LoPy4" in captured, captured
    assert "[LoRa] Starting LoRa Adapter" in captured, captured
    assert "Telemetry transport: CayenneLPP over LoRaWAN/TTN" in captured, captured
    assert "Telemetry status: SUCCESS (1/1)" in captured, captured

    # Check the raw LoRa payload.
    from mocket import Mocket
    assert Mocket.last_request() == bytearray(b'\x00g\x01\xbf\x00t\x01\xa4\x05z\x00\x0f\x05\ng\x01\xe1\x0bg\x01'
                                              b'\xe1\x05g\x00\x97\x05s)7\x05h\x9b\x00\x01\x00')

    # Check the value after decoding from CayenneLPP.
    from cayennelpp import LppFrame
    data = LppFrame.from_bytes(Mocket.last_request()).data

    # System temperature
    assert data[0].channel == 0
    assert data[0].type == 103
    assert data[0].value == (44.7,)

    # Voltage
    assert data[1].channel == 0
    assert data[1].type == 116
    assert data[1].value == (4.2,)

    assert data[2].channel == 5
    assert data[2].type == 122
    assert data[2].value == (3.845,)

    # DS18B20 temperature
    assert data[3].channel == 10
    assert data[3].type == 103
    assert data[3].value == (48.1,)
    assert data[4].channel == 11
    assert data[4].type == 103
    assert data[4].value == (48.1,)

    # BME280 temperature
    assert data[5].channel == 5
    assert data[5].type == 103
    assert data[5].value == (15.1,)

    # BME280 pressure
    assert data[6].channel == 5
    assert data[6].type == 115
    assert data[6].value == (1055.1,)

    # BME280 humidity
    assert data[7].channel == 5
    assert data[7].type == 104
    assert data[7].value == (77.5,)

    # EOF?
    assert data[8].channel == 0
    assert data[8].type == 1
    assert data[8].value == (0,)

    assert "[LoRa] No downlink message processed" in captured, captured


@pytest.mark.telemetry
@pytest.mark.lorawan
def test_downlink_interval_set(mocker, network_lora, caplog):
    """
    Simulate a downlink "set interval" command on LoRaWAN port 1.
    """

    mocker.patch("sys.platform", "LoPy4")

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
def test_downlink_interval_reset(mocker, network_lora, caplog):
    """
    Simulate a downlink "reset interval" command on LoRaWAN port 1.
    """

    mocker.patch("sys.platform", "LoPy4")

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
def test_downlink_pause(mocker, network_lora, caplog):
    """
    Simulate a downlink "pause" command on LoRaWAN port 2.
    """

    mocker.patch("sys.platform", "LoPy4")

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
def test_downlink_unpause(mocker, network_lora, caplog):
    """
    Simulate a downlink "unpause" command on LoRaWAN port 2.
    """

    mocker.patch("sys.platform", "LoPy4")

    # Define artificial LoRa conversation.
    network_lora.register_conversation(response_port=2, response_data=[b'\x00'])

    # Invoke datalogger with LoRaWAN telemetry settings for a single duty cycle.
    from test.settings import telemetry_lorawan
    invoke_datalogger_pycom(caplog, settings=telemetry_lorawan)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert '[LoRa] Received "pause payload submission" command: False' in captured, captured
