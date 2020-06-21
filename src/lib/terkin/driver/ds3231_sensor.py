# -*- coding: utf-8 -*-
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import SensorManager, AbstractSensor
from DS3231tokei import DS3231
from machine import RTC

log = logging.getLogger(__name__)


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create DS3231 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = DS3231Sensor(settings=sensor_info)
    sensor_bus = sensor_manager.get_bus_by_name(sensor_info.get('bus'))
    sensor_object.acquire_bus(sensor_bus)

    return sensor_object


class DS3231Sensor(AbstractSensor):
    """
    A generic DS3231 sensor/actor component.
    The DS3231 has a RTC which can be read & set. It also has a good temperature sensor.
    If the battery on the RTC has to be changed the time is set to 1.1.2000, 0.00h
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        # from terkin/sensor/core.py class AbstractSensor
        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.address = 0x68

    def start(self):
        """ Getting the bus """
        if self.bus is None:
            raise KeyError("Bus missing for DS3231")

        # Initialize the hardware driver.
        try:
            self.driver = DS3231(i2c=self.bus.adapter)
            return True

        except Exception as ex:
            log.exc(ex, 'DS3231 hardware driver failed')

        # set date/time of RTC
        self.set_time()

    def read(self):
        """ the DS3231 has a sensor for temperature compensation """

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        #log.info('Acquire reading from DS3231')

        data = {}

        temperature = self.driver.getTemperature()

        # Prepare readings.
        values = {
            "temperature": temperature,
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

    def set_time(self):
        """ set the system time to RTC time """

        rtc = RTC()
        [year,month,day,dotw,hour,minute,second] = self.driver.getDateTime() # get the date/time from the DS3231
        if year > 2019: # check valid data 
            rtc.init((year,month,day,dotw,hour,minute,second,0))    # set date/time
            log.debug("Time set:     {}".format(rtc.datetime()))
        else:
            log.warning("DS3231 date/time not set, not setting RTC")



    