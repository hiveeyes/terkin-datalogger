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


class VEDirectSensor(AbstractSensor):
    """
    A generic VEDirect sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.device = settings['device']
        self.timeout = 10
        self.driver = None

    def start(self):
        """Getting the bus"""

        # Initialize the hardware driver.
        try:

            # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                log.info('VEDirect on MicroPython not available at the moment')

            # CPython SerialBus EPSolar
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from terkin.lib.vedirect import Vedirect
                self.driver = Vedirect(device=self.device, timeout=self.timeout)
                log.info('Initialized Sensor VEDirect')

            else:
                raise NotImplementedError('VEDirect driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'VEDirect hardware driver failed')

    def read(self):
        """ """
        log.info('Initialized Reading Sensor VEDirect')
        log.info('Acquire reading from VEDirect')

        data = {}

        # Vanilla MicroPython 1.11 and Pycom MicroPython 1.9.4
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            log.info('implement usb/serial bus to VEDirect Device')

        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            data = self.driver.read_data_single()

        if not data:
            log.warning("Serial device {} has no value: {}".format(self.device, data))

        log.debug("Serial data:     {}".format(data))

        d = {}
        for key, value in data.items():
            key = 'vedirect:{}'.format(key)
            d[key] = value

        return d
