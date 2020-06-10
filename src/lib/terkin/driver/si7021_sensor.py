# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import SensorManager, AbstractSensor
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create SI7021 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = SI7021Sensor(settings=sensor_info)
    sensor_bus = sensor_manager.get_bus_by_name(sensor_info.get('bus'))
    sensor_object.acquire_bus(sensor_bus)

    return sensor_object


class SI7021Sensor(AbstractSensor):
    """
    A generic SI7021 sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.address = self.settings.get('address', 0x40)

    def start(self):
        """Getting the bus"""
        if self.bus is None:
            raise KeyError("Bus missing for SI7021Sensor")

        # Initialize the hardware driver.
        try:

            # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                from SI7021 import SI7021
                self.driver = SI7021(i2c=self.bus.adapter)

            # Adafruit CircuitPython
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                import adafruit_si7021
                self.driver = adafruit_si7021.SI7021(i2c_bus=self.bus.adapter, address=self.address)

            else:
                raise NotImplementedError('Si7021 driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'SI7021 hardware driver failed')

    def read(self):
        """ """

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        #log.info('Acquire reading from SI7021')

        data = {}

        # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:

            # Prepare readings.
            values = {
                "temperature": self.driver.temperature(),
                "humidity": self.driver.humidity(),
            }

        # Adafruit CircuitPython
        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:

            values = {
                "temperature": self.driver.temperature,
                "humidity": self.driver.relative_humidity,
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

