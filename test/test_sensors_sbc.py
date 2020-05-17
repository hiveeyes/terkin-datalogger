# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import mock
import pytest
from test.util.terkin import invoke_datalogger_raspberrypi


@pytest.mark.sensors
@pytest.mark.sbc
@mock.patch('adafruit_blinka.agnostic.board_id', "RASPBERRY_PI_4B")
@mock.patch('adafruit_blinka.agnostic.chip_id', "BCM2XXX")
@mock.patch('adafruit_platformdetect.board.Board.any_raspberry_pi_40_pin', True)
@mock.patch('adafruit_platformdetect.board.Board.any_embedded_linux', True)
def test_sensors_sbc(mocker, caplog):
    """
    Check the whole sensor machinery.
    """

    # Acquire minimal settings.
    from test.settings import sensors_sbc as sensor_settings

    # Invoke datalogger for a single duty cycle.
    datalogger = invoke_datalogger_raspberrypi(caplog, settings=sensor_settings)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert "Found 2 I2C devices: [118, 119]" in captured, captured
    assert "Found 2 1-Wire (DS18x20) devices: ['28ff641d8fdf18c1', '28ff641d8fc3944f']" in captured, captured

    # Get hold of the last reading.
    last_reading = datalogger.storage.last_reading

    # Proof it works by verifying last sensor readings.

    # BME280
    assert last_reading['temperature.0x77.i2c:0'] == 15.0994140625
    assert last_reading['humidity.0x77.i2c:0'] == 74.75231831647366
    assert last_reading['pressure.0x77.i2c:0'] == 1055.1656335994433

    # DS18B20
    assert last_reading['temperature.28ff641d8fdf18c1.onewire:0'] == 48.187
    assert last_reading['temperature.28ff641d8fc3944f.onewire:0'] == 48.187
