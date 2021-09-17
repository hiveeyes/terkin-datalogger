# https://github.com/nznobody/vedirect/blob/master/tests/conftest.py
from pytest import fixture
from unittest.mock import patch, Mock
import dummyserial
import logging
from serial import SerialBase


@fixture(scope="function")
def fake_serial():
    dummy = dummyserial.Serial(port="COM50", baudrate=9600)
    dummy.flushInput = Mock()
    dummy.reset_input_buffer = Mock()
    dummy._logger.setLevel(logging.INFO)
    with patch("serial.Serial", spec=SerialBase) as mock:
        # All possible parameters
        mock.return_value = dummy
        yield dummy
