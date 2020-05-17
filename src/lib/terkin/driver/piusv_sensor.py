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
    Create PiUSV+ sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = PiUSVSensor(settings=sensor_info)
    return sensor_object


class PiUSVSensor(AbstractSensor):
    """
    About
    =====
    PiUSV+ sensor component.

    Supported devices
    =================
    - PiUSV+ v. 1.0

    Resources
    =========
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        self.driver = None

    def start(self):
        log.info('Initializing sensor "PiUSV+"')

        # Initialize the hardware driver.
        try:

            # CPython
            if platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from rpi_piusv import PiUSV
                import smbus
                bus = smbus.SMBus(1)

                # Patch status definition for old firmwares. Unklar!
                PiUSV.status_definition['usb_power'] = 0x02
                PiUSV.status_definition['external_power'] = 0x01

                self.driver = PiUSV(bus)

                #print('Firmware version:', self.driver.read_firmware_version())
                # print('Data:', self.driver.read())

            else:
                raise NotImplementedError('PiUSV+ driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'PiUSV+ hardware driver failed')

    def read(self):

        log.info('Reading sensor "PiUSV+"')

        # CPython
        if platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            data_raw = self.driver.read()

            data = {}
            for key, value in data_raw.items():
                key = 'piusv:{}'.format(key)
                data[key] = value

            return data
        else:
            return none
