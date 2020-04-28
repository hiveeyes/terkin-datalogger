# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import AbstractSensor
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()


class EPSolarSensor(AbstractSensor):
    """
    A generic EPSolar sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.device = settings['device']
        self.driver = None

    def start(self):
        """Getting the bus"""
        # Initialize the hardware driver.

        log.info('Initializing sensor "EPSolar"')
        try:
            # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                raise NotImplementedError('Epsolar driver not implemented on MicroPython')

            # CPython SerialBus EPSolar
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from terkin.lib.epsolar import Epsolar
                self.driver = Epsolar(device=self.device)

            else:
                raise NotImplementedError('Epsolar driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'EPSolar hardware driver failed')

    def read(self):
        """ """
        log.info('Reading sensor "EPSolar"')
        log.info('Acquire reading from EPSolar')

        data = {}

        # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            raise NotImplementedError('Epsolar driver not implemented on MicroPython')

        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            serial_data, serial_read = self.driver.read_serial()
            serial_data_converted = self.driver.decode_serial(serial_data)
            serial_data_decoded = self.driver.serial_data_prepare(serial_data_converted)
            #serial_data_prepared = self.driver.serial_data_prepare(serial_data)
            data = serial_data_decoded

        if not data:
            log.warning("Serial device {} has no value: {}".format(self.device, data))

        log.debug("Serial data:     {}".format(data))

        d = {}
        for key, value in data.items():
            key = 'epsolar.{}'.format(key)
            d[key] = value

        return d
