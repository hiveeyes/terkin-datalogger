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

        # TODO: Review device reading re. glitches and timing.
        log.info('Acquire readings from all DS18X20 sensors attached to bus "{}"'.format(self.bus.name))
        devices = self.start_reading()
        time.sleep(1)
        data = self.read_devices(devices)

        if not data:
            log.warning('No data from any DS18X20 devices on bus "{}"'.format(self.bus.name))

        log.debug('Data from 1-Wire bus "{}" is "{}"'.format(self.bus.name, data))

        return data

    def start_reading(self):

        log.info('Start conversion for DS18X20 devices on bus "{}"'.format(self.bus.name))
        effective_devices = []
        for device in self.bus.devices:

            address = OneWireBus.device_address_ascii(device)
            device_settings = self.get_device_settings(address)

            enabled = device_settings.get('enabled')
            if enabled is False:
                log.info('Skipping DS18X20 device "{}"'.format(address))
                continue

            self.driver.start_conversion(device)

            effective_devices.append(device)

        return effective_devices

    def read_devices(self, devices):

        data = {}
        for device in devices:

            address = OneWireBus.device_address_ascii(device)
            log.info('Reading DS18X20 device "{}"'.format(address))
            try:
                value = self.driver.read_temp_async(device)
            except:
                log.exception("Reading DS18X20 device {} failed".format(address))
                continue

            # Evaluate device response.
            if value is not None:

                try:
                    # Compute telemetry field name.
                    fieldname = self.format_fieldname('temperature', address)

                    # Apply value offset.
                    offset = self.get_setting(address, 'offset')
                    if offset is not None:
                        log.info('Adding offset {} to value {} from device "{}"'.format(offset, value, address))
                        value += offset

                    # Add value to telemetry message.
                    data[fieldname] = value

                except:
                    log.exception('Processing data from DS18X20 device "{}" failed'.format(address))
                    continue

            else:
                log.warning('No response from DS18X20 device "{}"'.format(address))

        return data

    def get_setting(self, address, name, default=None):
        settings = self.get_device_settings(address)
        value = settings.get(name, default)
        return value

    def get_device_settings(self, address):

        # Compute ASCII representation of device address.
        address = OneWireBus.device_address_ascii(address)

        # Get device-specific settings from configuration.
        for device_settings in self.settings.get('devices', []):
            if device_settings['address'].lower() == address:
                return device_settings

        return {}

    def get_device_description(self, address):
        device_settings = self.get_device_settings(address)
        return device_settings.get('description')
