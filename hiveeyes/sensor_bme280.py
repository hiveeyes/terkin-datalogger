# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import AbstractSensor
from bme280_float import BME280

log = logging.getLogger(__name__)


class BME280Sensor(AbstractSensor):
    """
    A generic BME280 sensor component.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.address = 0x76

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
            log.exc(ex, 'BME280 hardware driver failed')

    def read(self):

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        #log.info('Acquire reading from BME280')

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

        Obtains readings from BME280's (integer variant) ``read_compensated_data()`` method.


        Integer formats
        ===============

        Temperature
        -----------
        The temperature in hundredths of a degree Celsius.
        For example, the value 2534 indicates a temperature of 25.34 degrees.

        Pressure
        --------
        The atmospheric pressure. This 32-bit value consists of 24 bits
        indicating the integer value, and 8 bits indicating the fractional
        value. To get a value in Pascals, divide the return value by 256.
        For example, a value of 24674867 indicates 96386.2Pa, or 963.862hPa.

        Humidity
        --------
        The relative humidity. This 32-bit value consists of 22 bits
        indicating the integer value, and 10 bits indicating the fractional
        value. To get a value in %RH, divide the return  value by 1024.
        For example, a value of 47445 indicates 46.333%RH.

        -- https://github.com/robert-hh/BME280#integer-formats
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
