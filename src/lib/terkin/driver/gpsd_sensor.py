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
    Create Gpsd sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = GpsdSensor(settings=sensor_info)
    return sensor_object

class GpsdSensor(AbstractSensor):
    """
    A generic GPSD sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.address = None
        self.driver = None

    def start(self):
        """Getting the bus"""

        log.info('Initializing sensor GPSD')

        # Initialize the hardware driver.
        try:

            # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                raise NotImplementedError('No GPSD on MicroPython')

            # CPython SerialBus EPSolar
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from terkin.lib.gpsd import Gpsd
                self.driver = Gpsd()

            else:
                raise NotImplementedError('GPSD driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'GPSD hardware driver failed')

    def read(self):
        """ """
        log.info('Reading sensor GPSD')

        if self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            raise NotImplementedError('No GPSD on MicroPython')

        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            data = self.driver.read()
            d = {}
            for key, value in data.items():
                key = '{}.gpsd'.format(key)
                d[key] = value
            return d
