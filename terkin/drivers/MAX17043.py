# -*- coding: utf-8 -*-
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import AbstractSensor
from DFRobot_MAX17043 import MAX17043

log = logging.getLogger(__name__)


class MAX17043Sensor(AbstractSensor):
    """
    A generic MAX17043 sensor component.
    
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        # from terkin/sensor/core.py class AbstractSensor
        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.address = 0x36

    def start(self):
        """Getting the bus"""
        if self.bus is None:
            raise KeyError("Bus missing for MAX17043")

        # Initialize the hardware driver.
        try:
            self.driver = MAX17043(address=self.address, i2c=self.bus.adapter)
            return True

        except Exception as ex:
            log.exc(ex, 'MAX17043 hardware driver failed')

    def read(self):
        """ """

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        #log.info('Acquire reading from MAX17043')

        data = {}

        t, p, h = self.driver.read_compensated_data()

        # Prepare readings.
        values = {
            "temperature": t,
            "pressure": p / 100,
            "humidity": h,
        }

        # Build telemetry payload.
        fieldnames = values.keys()
        for name in fieldnames:
            fieldname = self.format_fieldname(name, hex(self.address))
            value = values[name]
            data[fieldname] = value

        if not data:
            log.warning("I2C device {} has no value: {}".format(self.address, data))

        log.debug("I2C data:     {}".format(data))

        return data

    @staticmethod
    def int_to_float(t, p, h):
        """

        :param t: 
        :param p: 
        :param h: 

        """
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

        return values
