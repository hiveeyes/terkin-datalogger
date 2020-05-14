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
    Create VE.Direct sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = VEDirectSensor(settings=sensor_info)
    return sensor_object


class VEDirectSensor(AbstractSensor):
    """
    About
    =====
    Victron Energy VE.Direct MPPT charge controller sensor component.

    Supported devices
    =================
    - SmartSolar MPPT 100/20
    - SmartSolar MPPT 75/15
    - BlueSolar MPPT 75/15
    - BMV 702 battery monitor

    Resources
    =========
    - https://github.com/karioja/vedirect
    - https://www.victronenergy.com/solar-charge-controllers/smartsolar-mppt-75-10-75-15-100-15-100-20
    - https://www.victronenergy.com/solar-charge-controllers/bluesolar-mppt-150-35
    - https://www.victronenergy.com/battery-monitors/bmv-700
    - https://www.victronenergy.com/live/victronconnect:mppt-solarchargers

    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.device = settings['device']
        self.timeout = 5
        self.driver = None

    def start(self):
        log.info('Initializing sensor "Victron Energy VE.Direct"')

        # Initialize the hardware driver.
        try:

            # MicroPython
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                raise NotImplementedError('VEDirect driver not implemented on MicroPython')

            # CPython
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from vedirect import Vedirect
                self.driver = Vedirect(serialport=self.device, timeout=self.timeout)

            else:
                raise NotImplementedError('VEDirect driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'VEDirect hardware driver failed')

    def read(self):
        log.info('Reading sensor "Victron Energy VE.Direct"')

        # MicroPython
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            raise NotImplementedError('VEDirect driver not implemented on MicroPython')

        # CPython
        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            data_raw = self.driver.read_data_single()

        data = {}
        for key, value in data_raw.items():
            key = 'vedirect:{}'.format(key)
            data[key] = value

        return data
