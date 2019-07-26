# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from binascii import hexlify

from terkin import logging
from terkin.sensor import AbstractSensor
from terkin.sensor.core import OneWireBus

log = logging.getLogger(__name__)


class DS18X20Sensor(AbstractSensor):
    """
    A generic DS18B20 sensor component.
    """

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

        # TODO: Review device reading re. glitches and timing.
        log.info('Acquire readings from all DS18X20 sensors attached to bus {}'.format(self.bus.name))
        for device in self.bus.devices:
            try:
                self.read_single(data, device)
            except:
                log.exception("Reading DS18X20 device failed")

        if not data:
            log.warning("No data from any DS18X20 devices on bus {}".format(self.bus.name))

        log.debug("Onewire data: {}".format(data))

        return data

    def read_single(self, data, device):

        # Compute ASCII representation of device address.
        address = hexlify(device).decode()

        enabled = self.get_setting(address, 'enabled')
        if enabled is False:
            log.info("Skipping DS18X20 device {}".format(address))
            return

        log.info("Reading DS18X20 device {}".format(address))
        self.driver.start_conversion(device)
        time.sleep(1)
        value = self.driver.read_temp_async(device)

        # Evaluate device response.
        if value is not None:

            # Compute telemetry field name.
            fieldname = self.format_fieldname('temperature', address)

            # Apply value offset.
            offset = self.get_setting(address, 'offset')
            if offset is not None:
                log.info('Adding offset {} to value {} from sensor {}'.format(offset, value, address))
                value += offset

            # Add value to telemetry message.
            data[fieldname] = value

        else:
            log.warning("No response from DS18X20 device {}".format(address))

        time.sleep(1)

    def get_setting(self, address, name):
        device_settings = self.settings.get('devices', {})
        value = device_settings.get(address, {}).get(name)
        return value
