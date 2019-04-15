# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from binascii import hexlify

from terkin import logging
from terkin.sensor import AbstractSensor

log = logging.getLogger(__name__)


class DS18X20Sensor(AbstractSensor):
    """
    A generic DS18B20 sensor component.
    """

    def __init__(self):
        super().__init__()

        # The driver instance.
        self.bus = None
        self.driver = None

    def acquire_bus(self, bus):
        self.bus = bus

    def start(self):
        if self.bus is None:
            raise KeyError("Bus missing for DS18X20Sensor")

        # Initialize the DS18x20 hardware driver.
        try:
            from onewire.onewire import DS18X20
            self.driver = DS18X20(self.bus.adapter)
            return True

        except Exception as ex:
            log.exception('DS18X20 hardware driver failed')

    def read(self):

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        data = {}
        #log.info('Acquire reading from DS18X20')
        # for loop goes here
        for device in self.bus.devices:
            address = hexlify(device).decode()
            self.driver.start_conversion(device)
            time.sleep(0.750)
            value = self.driver.read_temp_async(device)
            if value is not None:
                fieldname = self.format_fieldname('temperature', address)
                data[fieldname] = value
            else:
                log.warning("Reading DS18X20 device {} failed".format(address))

            time.sleep(0.750)

        if not data:
            log.warning("No data from any DS18X20 devices on bus {}".format(self.bus.name))

        log.debug("Onewire data: {}".format(data))

        return data
