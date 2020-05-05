# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import SensorManager, AbstractSensor
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()

def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create GPIOZero sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = GPIOZeroSensor(settings=sensor_info)
    return sensor_object

class GPIOZeroSensor(AbstractSensor):
    """
    A generic GPIOZero sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.address = None
        self.cputemp = None
        self.loadaverage = None
        self.diskusage = None

    def start(self):
        """Getting the bus"""

        log.info('Initializing sensor GPIOZero')

        # Initialize the hardware driver.
        try:

            # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                raise NotImplementedError('No GPIOZero on MicroPython')

            # CPython SerialBus EPSolar
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from gpiozero import CPUTemperature, LoadAverage, DiskUsage
                self.cputemp = CPUTemperature(min_temp=50, max_temp=90)
                self.loadaverage = LoadAverage(min_load_average=0, max_load_average=2)
                self.diskusage = DiskUsage()

            else:
                raise NotImplementedError('GPIOZero driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'GPIOZero hardware driver failed')

    def read(self):
        """ """
        log.info('Reading sensor GPIOZero')

        if self.cputemp is None:
            return self.SENSOR_NOT_INITIALIZED

        # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            raise NotImplementedError('No GPIOZero on MicroPython')

        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            data = {'cputemp': format(self.cputemp.temperature),
                    'diskusage': format(self.diskusage.usage),
                    'loadaverage': format(self.loadaverage.load_average)}
            print('GPIOZero Data:', data)
            d = {}
            for key, value in data.items():
                key = '{}.rpi'.format(key)
                d[key] = value
            return d
