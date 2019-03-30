# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from binascii import hexlify
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

        # Can be overwritten by ``.set_address()``.
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

        log.info('Acquire reading from BME280')

        data = {}

        t, p, h = self.driver.read_compensated_data()

        # Prepare readings.
        values = {}
        if t:
            values["temperature"] = t / 100

        if p:
            p = p // 256
            pi = p // 100
            pd = p - pi * 100
            values["pressure"] = float("{}.{:02d}".format(pi, pd))

        if h:
            hi = h // 1024
            hd = h * 100 // 1024 - hi * 100
            values["humidity"] = float("{}.{:02d}".format(hi, hd))

        # Build telemetry payload.
        fieldnames = values.keys()
        for name in fieldnames:
            #print('self.bus', self.bus)
            #print('dir self.bus', dir(self.bus))
            fieldname = '{name}.{bus}.{address}'.format(name=name, bus=self.bus.name, address=hex(self.address))
            value = values[name]
            data[fieldname] = value

        if not data:
            log.warning("I2C device {} has no value: {}".format(self.address, data))

        log.info("I2C data: {}".format(data))

        return data
