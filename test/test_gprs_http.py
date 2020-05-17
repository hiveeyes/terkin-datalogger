# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import mock
import pytest
import logging
from test.util.terkin import invoke_datalogger

logger = logging.getLogger(__name__)


@pytest.fixture
def sim800mock():

    # TODO: Make it answer to real AT-command conversations.
    import pythings_sim800
    #mock.patch('pythings_sim800.Modem.get_ip_addr', mock.Mock(return_value='192.168.111.42'))
    pythings_sim800.Modem.get_ip_addr = mock.Mock(return_value='192.168.111.42')

    def execute_at_command(self, command, data=None, clean_output=True):

        if command == 'modeminfo':
            return 'SIM800 R14.08'
        elif command == 'initurl':
            assert data == 'https://daq.example.org/api/workbench/testdrive/area-42/node-01-http-json/data', data
        elif command == 'dumpdata':
            assert '"system.memfree": 1000000' in data, data
            assert '"system.temperature": 44.7053182608696' in data, data
            assert '"temperature.0x77.i2c:0": 15.129645347595215' in data, data
            assert '"temperature.28ff641d8fc3944f.onewire:0": 48.1875' in data, data

        elif command == 'dopost':
            return 'OK,200'

        return 'MOCKVOID'

    pythings_sim800.Modem.execute_at_command = execute_at_command


@pytest.mark.telemetry
@pytest.mark.gprs
@mock.patch('sys.platform', 'esp32')
def test_uplink_gprs_http(caplog, sim800mock):
    """
    Pretend to invoke the datalogger on a TTGO T-Call with some sensors.

    By intercepting the Pythings SIM800 driver, proof that the submitted
    payload is correct. Also, check log output.
    """

    # Mix together different settings.
    from test.settings import telemetry_gprs
    from test.settings import sensors_micropython as sensor_settings
    telemetry_gprs.sensors = sensor_settings.sensors

    # Invoke datalogger with LoRaWAN telemetry settings for a single duty cycle.
    invoke_datalogger(caplog, settings=telemetry_gprs)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert "Starting Terkin datalogger" in captured, captured
    assert "platform: esp32" in captured, captured
    assert "[GPRS] Starting GPRS Manager" in captured, captured
    assert "Telemetry transport: JSON over HTTP over GPRS" in captured, captured
    assert "Telemetry status: SUCCESS (1/1)" in captured, captured
