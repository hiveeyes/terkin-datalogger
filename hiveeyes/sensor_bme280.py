# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import AbstractSensor
from bme280 import BME280

log = logging.getLogger(__name__)


class BME280Sensor(AbstractSensor):
    """
    A generic BME280 sensor component.
    """

    def __init__(self):
        super().__init__()

        # The driver instance.
        self.bus = None

        # TODO: Get sensors i2c bus address from settings.
        self.address = 0x76

        self.driver = None

    def start(self):
        """
        Getting the bus
        """
        if self.bus is None:
            raise KeyError("Bus missing for BME280Sensor")

        # Initialize the hardware driver.
        try:
            self.driver = BME280(address=self.address, i2c=self.bus.adapter)
            return True

        except Exception as ex:
            log.exception('BME280 hardware driver failed')

    def read(self):

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        data = {}
        log.info('Acquire reading from BME280')

        t, p, h = self.driver.read_compensated_data()

        # TODO: Review this.
        if t and p and h:

            p = p // 256
            pi = p // 100
            pd = p - pi * 100

            hi = h // 1024
            hd = h * 100 // 1024 - hi * 100

            data["temperature"] = t / 100
            data["humidity"] = float("{}.{:02d}".format(hi, hd))
            data["pressure"] = float("{}.{:02d}".format(pi, pd))

            # TODO: add bus identifier DYNAMICLY into <SENSOR_NAME> as well. e.g. temperature_i2c:0:0x77
            #temp_name = "temperature_i2c:0:" + str(self.address)
            #hum_name = "humidity_i2c:0:" + str(self.address)
            #pres_name = "pressure_i2c:0:" + str(self.address)
            #data[temp_name] = t / 100
            #data[hum_name] = float("{}.{:02d}".format(hi, hd))
            #data[pres_name] = float("{}.{:02d}".format(pi, pd))

        else:
            log.warning("I2C device {} has no value".format(data))

        log.debug("I2C data: {}".format(data))

        return data
