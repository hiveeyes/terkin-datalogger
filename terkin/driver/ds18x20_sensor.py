# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time

from terkin import logging
from terkin.sensor import AbstractSensor
from terkin.sensor.core import OneWireBus
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()


class DS18X20Sensor(AbstractSensor):
    """
    A generic DS18B20 sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    """

    def acquire_bus(self, bus):
        """

        :param bus: 

        """
        self.bus = bus

    def start(self):
        """ """
        if self.bus is None:
            raise KeyError("Bus missing for DS18X20Sensor")

        # Initialize the DS18x20 hardware driver.
        onewire_bus = self.bus.adapter
        try:

            # Vanilla MicroPython 1.11
            if platform_info.vendor == platform_info.MICROPYTHON.Vanilla:
                import ds18x20
                self.driver = DS18X20NativeDriverAdapter(ds18x20.DS18X20(onewire_bus))

            # Pycom MicroPython 1.9.4
            elif platform_info.vendor == platform_info.MICROPYTHON.Pycom:
                from onewire_python import DS18X20
                self.driver = DS18X20(onewire_bus)

            else:
                raise NotImplementedError('DS18X20 driver not implemented on this platform')

        except Exception as ex:
            log.exc(ex, 'DS18X20 hardware driver failed')
            return False

        return True

    def read(self):
        """ """

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        # TODO: Review device reading re. glitches and timing.
        log.info('Acquire readings from all DS18X20 sensors attached to bus "{}"'.format(self.bus.name))
        devices = self.start_reading()
        time.sleep_ms(750)
        data = self.read_devices(devices)

        if not data:
            log.warning('No data from any DS18X20 devices on bus "{}"'.format(self.bus.name))

        log.debug('Data from 1-Wire bus "{}" is "{}"'.format(self.bus.name, data))

        return data

    def start_reading(self):
        """ """

        log.info('Start conversion for DS18X20 devices on bus "{}"'.format(self.bus.name))
        effective_devices = []
        for device in self.bus.devices:

            address = OneWireBus.device_address_ascii(device)
            device_settings = self.get_device_settings(address)

            enabled = device_settings.get('enabled')
            if enabled is False:
                log.info('Skipping DS18X20 device "{}"'.format(address))
                continue

            effective_devices.append(device)

        self.driver.start_conversion()

        return effective_devices

    def read_devices(self, devices):
        """

        :param devices: 

        """

        data = {}
        for device in devices:

            address = OneWireBus.device_address_ascii(device)
            log.info('Reading DS18X20 device "{}"'.format(address))
            try:
                value = self.driver.read_temp_async(device)
            except Exception as ex:
                log.exc(ex, "Reading DS18X20 device {} failed".format(address))
                continue

            # Evaluate device response.
            if value is not None:

                # TODO: Filter the 85° thing here.

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

                except Exception as ex:
                    log.exc(ex, 'Processing data from DS18X20 device "{}" failed'.format(address))
                    continue

            else:
                log.warning('No response from DS18X20 device "{}"'.format(address))

        return data

    def get_setting(self, address, name, default=None):
        """

        :param address: 
        :param name: 
        :param default:  (Default value = None)

        """
        settings = self.get_device_settings(address)
        value = settings.get(name, default)
        return value

    def get_device_settings(self, address):
        """

        :param address: 

        """

        # Compute ASCII representation of device address.
        address = OneWireBus.device_address_ascii(address)

        # Get device-specific settings from configuration.
        for device_settings in self.settings.get('devices', []):
            if device_settings['address'].lower() == address:
                return device_settings

        return {}

    def get_device_description(self, address):
        """

        :param address: 

        """
        device_settings = self.get_device_settings(address)
        return device_settings.get('description')


class DS18X20NativeDriverAdapter:
    """
    Adapter for mimicking the pure-Python onewire.py
    driver from the early days of MicroPython 1.9.4.

    https://github.com/pycom/pycom-libraries/blob/dabce8d9/examples/DS18X20/onewire.py
    """

    def __init__(self, driver):
        self.driver = driver

    def start_conversion(self):
        """
        Start the temp conversion on all DS18x20 devices.
        """
        return self.driver.convert_temp()

    def read_temp_async(self, rom):
        """
        Read the temperature from the scratch memory of one DS18x20 device
        if the conversion is complete, otherwise return None.
        """
        return self.driver.read_temp(rom)
