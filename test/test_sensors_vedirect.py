# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020-2021 Andreas Motl <andreas@hiveeyes.org>
# (c) 2021 Manu Lange <Manu.Lange@plantandfood.co.nz>
# License: GNU General Public License, Version 3
import sys
import types
import mock
import pytest
from test.util.terkin import invoke_datalogger_raspberrypi, invoke_datalogger_pycom

# https://github.com/nznobody/vedirect/blob/901ed6e/tests/vedirect_device_emulator.py#L61-L69
MPPT_DATA = '\r\nV\t12800\r\nVPV\t3350\r\nPPV\t130\r\nI\t15000\r\nIL\t1500\r\nLOAD\tON\r\nRelay\tOFF\r\nH19\t456\r\nH20\t45\r\nH21\t300\r\nH22\t45\r\nH23\t350\r\nERR\t0\r\nCS\t5\r\nFW\t1.19\r\nPID\t0xA042\r\nSER#\tHQ141112345\r\nHSDS\t0\r\nMPPT\t2\r\nChecksum\t\x99'


@pytest.mark.sensors
@pytest.mark.sbc
@mock.patch('adafruit_blinka.agnostic.board_id', "RASPBERRY_PI_4B")
@mock.patch('adafruit_blinka.agnostic.chip_id', "BCM2XXX")
@mock.patch('adafruit_platformdetect.board.Board.any_raspberry_pi_40_pin', True)
@mock.patch('adafruit_platformdetect.board.Board.any_embedded_linux', True)
def test_sensors_vedirect_sbc(mocker, caplog, fake_serial):
    """
    Check the whole sensor machinery.
    """

    fake_serial._waiting_data = MPPT_DATA

    # Acquire settings.
    from test.settings import sensors_vedirect_sbc as sensor_settings

    # Invoke datalogger for a single duty cycle.
    datalogger = invoke_datalogger_raspberrypi(caplog, settings=sensor_settings)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert 'Initializing sensor "Victron Energy VE.Direct" on "/dev/ttysdummy042"' in captured, captured

    # Get hold of the last reading.
    last_reading = datalogger.storage.last_reading

    # Proof it works by verifying last sensor readings.
    verify_reading(last_reading)


@pytest.mark.sensors
@pytest.mark.esp32
@mock.patch('sys.implementation', types.SimpleNamespace(_multiarch='micropython', name='micropython', cache_tag='micropython-1.14', version=sys.version_info))
def test_sensors_vedirect_mpy(mocker, caplog):

    # Define platform.
    mocker.patch("sys.platform", "esp32")

    import vedirect
    vedirect.vedirect.MICROPYTHON = True

    # Acquire settings.
    from test.settings import sensors_vedirect_mpy as sensor_settings

    # Invoke datalogger for a single duty cycle.
    datalogger = invoke_datalogger_pycom(caplog, settings=sensor_settings, after_setup=setup_dummy_uart)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert 'Initializing sensor "Victron Energy VE.Direct" on "1"' in captured, captured

    # Get hold of the last reading.
    last_reading = datalogger.storage.last_reading

    # Proof it works by verifying measurement values.
    verify_reading(last_reading)


def verify_reading(last_reading):
    assert last_reading['vedirect-0xA042:CS'] == 5
    assert last_reading['vedirect-0xA042:ERR'] == 0
    assert last_reading['vedirect-0xA042:FW'] == "1.19"
    assert last_reading['vedirect-0xA042:H19'] == 456
    assert last_reading['vedirect-0xA042:H20'] == 45
    assert last_reading['vedirect-0xA042:H21'] == 300
    assert last_reading['vedirect-0xA042:H22'] == 45
    assert last_reading['vedirect-0xA042:H23'] == 350
    assert last_reading['vedirect-0xA042:HSDS'] == 0
    assert last_reading['vedirect-0xA042:I'] == 15000
    assert last_reading['vedirect-0xA042:IL'] == 1500
    assert last_reading['vedirect-0xA042:LOAD'] == "ON"
    assert last_reading['vedirect-0xA042:MPPT'] == 2
    assert last_reading['vedirect-0xA042:PID'] == "0xA042"
    assert last_reading['vedirect-0xA042:PPV'] == 130
    assert last_reading['vedirect-0xA042:Relay'] == "OFF"
    assert last_reading['vedirect-0xA042:SER#'] == "HQ141112345"
    assert last_reading['vedirect-0xA042:V'] == 12800
    assert last_reading['vedirect-0xA042:VPV'] == 3350


def setup_dummy_uart(datalogger):
    """
    Patch UART interface to use a dummy one instead of a mocked one.
    """
    sens = datalogger.sensor_manager.get_sensor_by_id("vedirect-mpy-1")
    if sens:
        class DummyUART:

            def __init__(self):
                self.position = 0
                self.data = MPPT_DATA

            def read(self, count):
                char = MPPT_DATA[self.position]
                self.position += 1
                return bytes(char, "latin1")

        sens.driver.ser = DummyUART()
