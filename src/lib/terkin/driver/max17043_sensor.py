# -*- coding: utf-8 -*-
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import SensorManager, AbstractSensor

log = logging.getLogger(__name__)


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create MAX17043 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = MAX17043Sensor(settings=sensor_info)
    sensor_bus = sensor_manager.get_bus_by_name(sensor_info.get('bus'))
    sensor_object.acquire_bus(sensor_bus)

    return sensor_object


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
        self.address = self.settings.get('address', 0x36)

    def start(self):
        """Getting the bus"""
        if self.bus is None:
            raise KeyError("Bus missing for MAX17043")

        # Initialize the hardware driver.
        try:
            from max17043 import DFRobot_MAX17043 as MAX17043
            self.driver = MAX17043(i2c=self.bus.adapter)
            return True

        except Exception as ex:
            log.exc(ex, 'MAX17043 hardware driver failed')

    def read(self):
        """ """

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        #log.info('Acquire reading from MAX17043')

        data = {}

        voltage = self.driver.readVoltage()
        percentage = self.driver.readPercentage()

        # Prepare readings.
        values = {
            "voltage": voltage / 1000,
            "percentage": percentage,
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

    