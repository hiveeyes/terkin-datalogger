# -*- coding: utf-8 -*-
# (c) 2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2020 Andreas Motl <andreas.motl@terkin.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import SensorManager, AbstractSensor
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create EPSolar sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = EPSolarSensor(settings=sensor_info)
    return sensor_object


class EPSolarSensor(AbstractSensor):
    """
    About
    =====
    EPSolar ViewStar PWM charge controller sensor component.

    Supported devices
    =================
    - EPSolar ViewStar VS1024N with TTL232 interface and Tracer-MT-5 protocol.

    Resources
    =========
    - http://solpanelerotillbehor.se/Publications/Viewstar%20prod%20info%20140212.pdf
    - https://github.com/xxv/tracer
    - https://github.com/xxv/tracer/network
    - https://github.com/xxv/tracer/blob/master/docs/Protocol-Tracer-MT-5.pdf

    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.device = settings['device']
        self.driver = None

    def start(self):
        """
        Initialize the hardware driver for reading
        the EPSolar ViewStar PWM Charge Controller.
        """
        log.info('Initializing sensor "EPSolar"')

        try:

            # MicroPython
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                raise NotImplementedError('EPSolar driver not implemented on MicroPython')

            # CPython
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from terkin.lib.epsolar import EPSolar
                self.driver = EPSolar(device=self.device)

            else:
                raise NotImplementedError('EPSolar driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'EPSolar hardware driver failed')

    def read(self):
        """
        Read data from the EPSolar ViewStar PWM Charge Controller.
        """
        log.info('Reading sensor "EPSolar"')

        # MicroPython
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            raise NotImplementedError('EPSolar driver not implemented on MicroPython')

        # CPython
        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            serial_data, serial_read = self.driver.read_serial()
            serial_data_converted = self.driver.decode_serial(serial_data)
            serial_data_decoded = self.driver.serial_data_prepare(serial_data_converted)
            #serial_data_prepared = self.driver.serial_data_prepare(serial_data)
            data_raw = serial_data_decoded

        else:
            raise NotImplementedError('EPSolar driver not implemented on this platform')

        data = {}
        for key, value in data_raw.items():
            key = 'epsolar.{}'.format(key)
            data[key] = value

        return data
