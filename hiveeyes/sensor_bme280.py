# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3

from terkin.sensor import AbstractSensor
from bme280 import BME280

"""
# DS18B20 data line connected to pin P10

while True:
    print(temp.read_temp_async())
    time.sleep(1)
    temp.start_conversion()
    time.sleep(1)

"""

class BME280Sensor(AbstractSensor):
    """
    A generic DS18B20 sensor component.
    """

    def __init__(self):
        super().__init__()

        # The driver instance.
        self.readings = None
        self.sensor = None
        self.bus = None
        TODO: get sensors i2c bus address from settings
        self.address = 0x77

    def start(self):
        """
        Getting the bus
        """
        if self.bus is None:
            raise KeyError("Bus missing")

        # Initialize the hardware driver.
        try:
            self.sensor = BME280(address=self.address, i2c=self.bus.adapter)
        except Exception as ex:
            print('ERROR: BME280 hardware driver failed. {}'.format(ex))
            raise

    def read(self):
        data = {}
        print('INFO:  Acquire reading from BME280')

        t, p, h = self.sensor.read_compensated_data()
        if  t and p and h:

            p = p // 256
            pi = p // 100
            pd = p - pi * 100

            hi = h // 1024
            hd = h * 100 // 1024 - hi * 100

            data["temperature"] = t / 100
            data["humidity"] = float("{}.{:02d}".format(hi, hd))
            data["pressure"] = float("{}.{:02d}".format(pi, pd))
        else:
            print("WARNING: device {} has no value".format(data))

        print("I2C data: {}".format(data))

        return data



