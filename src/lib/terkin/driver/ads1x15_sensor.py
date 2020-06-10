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
    Create ADS1x15 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = ADS1x15Sensor(settings=sensor_info)
    sensor_bus = sensor_manager.get_bus_by_name(sensor_info.get('bus'))
    sensor_object.acquire_bus(sensor_bus)

    return sensor_object


class ADS1x15Sensor(AbstractSensor):
    """
    A generic ADS1x15 sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        self.handler = None
        self.driver = None
        self.channel = self.settings['channel']
        self.model = self.settings['model']

        # Can be overwritten by ``.set_address()``.
        self.address = self.settings.get('address', 0x48)

    def start(self):

        if self.bus is None:
            raise KeyError("Bus missing for ADS1x15 sensor")

        # Initialize the hardware driver.
        try:

            # MicroPython
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                # TODO: Integrate https://github.com/robert-hh/ads1x15 here.
                raise NotImplementedError('ADS1x15 driver not implemented on MicroPython')

            # CPython
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:

                # Select model.
                if self.model == 'ads1115':
                    import adafruit_ads1x15.ads1115 as ADS
                    driver_class = ADS.ADS1115
                elif self.model == 'ads1015':
                    import adafruit_ads1x15.ads1015 as ADS
                    driver_class = ADS.ADS1015
                else:
                    log.warning('ADS Model not supported')
                # Setup driver.
                from adafruit_ads1x15.analog_in import AnalogIn
                self.handler = driver_class(i2c=self.bus.adapter, address=self.address)
                self.driver = AnalogIn(self.handler, getattr(ADS, self.channel))

            else:
                raise NotImplementedError('ADS1x15 driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'ADS1x15 hardware driver failed')

    def read(self):

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        # MicroPython
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            raise NotImplementedError('ADS1x15 driver not implemented on MicroPython')

        # CPython
        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            values = {
                # "value_raw": self.driver.value,
                # "voltage_raw": self.driver.voltage,
                "voltage": self.driver.voltage * self.settings['multiplicator'],
            }

        # Build telemetry payload.
        data = {}
        for key, value in values.items():
            name = '{}.{}'.format(key, self.model)
            fieldname = self.format_fieldname(name, hex(self.address), self.channel.lower())
            data[fieldname] = value

        return data
