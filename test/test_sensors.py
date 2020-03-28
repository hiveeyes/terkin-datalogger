# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import mock
import pytest
from test.util.terkin import invoke_datalogger_pycom


@pytest.mark.sensors
@mock.patch('sys.platform', 'FiPy')
def test_sensors(mocker, caplog):
    """
    Check the whole sensor machinery.
    """

    # Acquire minimal settings.
    from test.settings import sensors as sensor_settings

    # Pretend the HX711 to be ready.
    mocker.patch('terkin.lib.hx711_heisenberg.HX711Heisenberg.is_ready', mock.Mock(return_value=True))

    # Invoke datalogger for a single duty cycle.
    datalogger = invoke_datalogger_pycom(caplog, settings=sensor_settings)

    # Capture log output.
    captured = caplog.text

    # Proof it works by verifying log output.
    assert "Found 2 I2C devices: [118, 119]." in captured, captured
    assert "Found 2 1-Wire (DS18x20) devices: ['28ff641d8fdf18c1', '28ff641d8fc3944f']" in captured, captured

    # Get hold of the last reading.
    last_reading = datalogger.storage.last_reading

    # Proof it works by verifying last sensor readings.

    # ADC
    assert last_reading['system.voltage.battery'] == 4.2

    # BME280
    assert last_reading['temperature.0x77.i2c:0'] == 15.129645347595215
    assert last_reading['humidity.0x77.i2c:0'] == 77.88673400878906
    assert last_reading['pressure.0x77.i2c:0'] == 1055.163671875

    # DS18B20
    assert last_reading['temperature.28ff641d8fc3944f.onewire:0'] == 48.1875
    assert last_reading['temperature.28ff641d8fdf18c1.onewire:0'] == 48.1875

    # HX711
    assert last_reading['weight.0'] == 3.845
