# -*- coding: utf-8 -*-
# (c) 2019-2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.model import SensorReading
from terkin.sensor import SensorManager, AbstractSensor
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create BMP280 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = BMP280Sensor(settings=sensor_info)
    sensor_bus = sensor_manager.get_bus_by_name(sensor_info.get('bus'))
    sensor_object.acquire_bus(sensor_bus)

    return sensor_object


class BMP280Sensor(AbstractSensor):
    """
    A generic BMP280 sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.address = self.settings.get('address', 0x76)

    def start(self):
        """
        Setup the BMP280 sensor driver.

        :return:
        """

        # Ensure a bus object exists and is ready.
        self.ensure_bus()

        # Initialize the hardware driver.
        try:

            # MicroPython
            # https://github.com/dafvid/micropython-bmp280

            # Adafruit CircuitPython
            if platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                import adafruit_bmp280
                self.driver = adafruit_bmp280.Adafruit_BMP280_I2C(i2c=self.bus.adapter, address=self.address)

            else:
                raise NotImplementedError('BMP280 driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'BMP280 hardware driver failed')
            return False

    def read(self):
        """
        Read the BMP280 sensor.

        :return: SensorReading
        """

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        #log.info('Acquire reading from BMP280')

        data = {}

        # Adafruit CircuitPython
        if platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:

            values = {
                "temperature": self.driver.temperature,
                "pressure": self.driver.pressure,
            }

        # Build telemetry payload.
        # TODO: Push this further into the telemetry domain.
        fieldnames = values.keys()
        for name in fieldnames:
            fieldname = self.format_fieldname(name, hex(self.address))
            value = values[name]
            data[fieldname] = value

        if not data:
            log.warning("I2C device {} has no value: {}".format(self.address, data))

        log.debug("I2C data:     {}".format(data))

        reading = SensorReading()
        reading.sensor = self
        reading.data = data

        return reading
