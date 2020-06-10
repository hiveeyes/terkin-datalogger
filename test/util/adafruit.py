import sys
import adafruit_bme280
from adafruit_blinka.microcontroller.generic_linux.i2c import I2C


class MockedI2C(I2C):

    def scan(self):
        return [0x76, 0x77]

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):

        self.register = None

        if address in [0x76, 0x77]:
            if buffer:
                self.register = buffer[0]
        else:
            raise KeyError('Unknown I2C device {}'.format(hex(address)))

    def readfrom_into(self, address, buffer, *, start=0, end=None, stop=True):

        addr = address

        result = None
        if addr in [0x76, 0x77]:

            memaddr = self.register

            # Device probing.
            if memaddr == 0x00:
                result = bytearray([])

            elif memaddr == adafruit_bme280._BME280_REGISTER_CHIPID:
                result = bytearray([adafruit_bme280._BME280_CHIPID])

            # BME280 calibration for temperature and pressure.
            elif memaddr == 0x88:
                result = bytearray([
                    # T1-3
                    0x01, 0x02, 0x03, 0x04, 0xaa, 0x06,
                    # P1-4
                    0xff, 0x60, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00,
                    # P5-9
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                    # _, H1
                    0x00, 0x00])

            # BME280 calibration for humidity.
            elif memaddr == 0xA1:
                result = bytearray([0xff])

            elif memaddr == 0xE1:
                result = bytearray([0xff, 0x02, 0x00, 0x20, 0x00, 0x00, 0x00])

            # BME280_REGISTER_STATUS
            elif memaddr == 0xF3:
                result = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

            # BME280 temperature readout
            elif memaddr == 0xFA:
                result = bytearray([0x99, 0xbb, 0x03])

            # BME280 humidity readout
            elif memaddr == 0xFD:
                result = bytearray([0x99, 0xee])

            # BME280 burst readout
            # TODO: Individualize this pre BME280 instance.
            elif memaddr == 0xF7:
                result = bytearray([0x99, 0xbb, 0x03, 0x99, 0xee, 0xff, 0x99, 0xff])

        if result is not None:

            if end is None:
                end = len(buffer)

            for i in range(end - start):
                buffer[i + start] = result[i]

        else:
            raise KeyError('Unknown I2C memory address {} on device {}'.format(hex(memaddr), hex(addr)))


def monkeypatch():
    sys.modules['adafruit_blinka'].microcontroller.generic_linux.i2c.I2C = MockedI2C
