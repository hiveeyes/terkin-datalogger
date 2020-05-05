# -*- coding: utf-8 -*-
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from terkin import logging
from terkin.sensor import SensorManager, AbstractSensor
from terkin.util import get_platform_info

log = logging.getLogger(__name__)


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create DS18x20 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = DS18x20Sensor(settings=sensor_info)
    sensor_bus = sensor_manager.get_bus_by_name(sensor_info.get('bus'))
    sensor_object.acquire_bus(sensor_bus)
    return sensor_object


class DS18x20Sensor(AbstractSensor):
    """
    A generic DS18B20 sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory
    """

    def start(self):
        """
        Setup the DS18x20 sensor driver.
        :return:
        """

        # Ensure a bus object exists and is ready.
        self.ensure_bus()

        # Initialize the DS18x20 hardware driver.
        onewire_bus = self.bus.adapter
        try:

            use_native_driver = self.bus.settings.get('driver') == 'native'

            platform_info = get_platform_info()

            # Vanilla MicroPython 1.11
            if platform_info.vendor == platform_info.MICROPYTHON.Vanilla or use_native_driver:
                import ds18x20_native
                self.driver = ds18x20_native.DS18X20(onewire_bus)

            # Pycom MicroPython 1.9.4
            elif platform_info.vendor == platform_info.MICROPYTHON.Pycom:
                import ds18x20_python
                self.driver = ds18x20_python.DS18X20(onewire_bus)

            # RaspberryPi
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from terkin.sensor.linux import LinuxSysfsDS18B20
                self.driver = LinuxSysfsDS18B20(onewire_bus)

            else:
                raise NotImplementedError('DS18x20 driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'DS18x20 hardware driver failed')
            return False

    def read(self):
        """
        - Start conversion on all DS18x20 sensors.
        - Wait for conversion.
        - Read all DS18x20 sensors.
        """

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        log.info('Acquire readings from all DS18x20 sensors attached to bus "{}"'.format(self.bus.name))

        # Start conversion on all DS18x20 sensors.
        self.driver.convert_temp()
        time.sleep_ms(750)

        # Read scratch memory of each sensor.
        data = self.read_devices()

        if not data:
            log.warning('No data from any DS18x20 devices on bus "{}"'.format(self.bus.name))

        log.debug('Data from 1-Wire bus "{}" is "{}"'.format(self.bus.name, data))

        return data

    def get_effective_devices(self):
        """
        Return list of all DS18x20 devices.
        """

        log.info('Start conversion for DS18x20 devices on bus "{}"'.format(self.bus.name))
        effective_devices = []
        for device in self.bus.devices:

            address = self.bus.device_address_ascii(device)
            device_settings = self.get_device_settings(address)

            enabled = device_settings.get('enabled')
            if enabled is False:
                log.info('Skipping DS18x20 device "{}"'.format(address))
                continue

            effective_devices.append(device)

        return effective_devices

    def read_devices(self):
        """
        Read all DS18x20 sensors and return data dictionary.
        """

        data = {}
        devices = self.get_effective_devices()
        for device in devices:

            address = self.bus.device_address_ascii(device)
            log.info('Reading DS18x20 device "{}"'.format(address))
            try:
                value = self.driver.read_temp(device)
            except Exception as ex:
                log.exc(ex, "Reading DS18x20 device {} failed".format(address))
                continue

            # Evaluate device response.
            if value is not None:

                # TODO: Mask power-on reset value 0550h (85°) here.
                # https://github.com/micropython/micropython/pull/5338
                # Maybe it's not only 85°. Sometimes it's also 25°(!).
                # https://github.com/cpetrich/counterfeit_DS18B20

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
                    log.exc(ex, 'Processing data from DS18x20 device "{}" failed'.format(address))
                    continue

            else:
                log.warning('No response from DS18x20 device "{}"'.format(address))

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
        address = self.bus.device_address_ascii(address)

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
