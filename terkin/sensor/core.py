# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from binascii import hexlify
from machine import Pin, I2C

from terkin import logging

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)


class SensorManager:
    """
    Manages all busses and sensors.
    """

    def __init__(self):
        self.sensors = []
        self.busses = {}

    def register_sensor(self, sensor):
        self.sensors.append(sensor)

    def register_bus(self,  bus):
        bus_name = bus.name
        log.info('Registering bus "%s"', bus_name)
        self.busses[bus_name] = bus

    def get_bus_by_name(self, name):
        log.info('Trying to find bus by name "%s"', name)
        bus = self.busses.get(name)
        log.info('Found bus by name "%s": %s', name, bus)
        return bus

    def get_sensor_by_name(self, name):
        raise NotImplementedError('"get_sensor_by_name" not implemented yet')

    def setup_busses(self, busses_settings):
        """
        Register configured I2C, OneWire and SPI busses.
        """
        log.info("Starting all busses %s", busses_settings)
        for bus_settings in busses_settings:

            if bus_settings.get("enabled") is False:
                log.info('Bus with id "{}" and family "{}" is disabled, '
                         'skipping registration'.format(bus_settings.get('id'), bus_settings.get('family')))
                continue

            try:
                self.setup_bus(bus_settings)
            except:
                log.exception('Registering bus failed. settings={}'.format(bus_settings))

    def setup_bus(self, bus_settings):
        bus_family = bus_settings.get('family')

        if bus_family == BusType.OneWire:
            owb = OneWireBus(bus_settings)
            owb.register_pin("data", bus_settings['pin_data'])
            owb.start()
            self.register_bus(owb)

        elif bus_family == BusType.I2C:
            i2c = I2CBus(bus_settings)
            i2c.register_pin("sda", bus_settings['pin_sda'])
            i2c.register_pin("scl", bus_settings['pin_scl'])
            i2c.start()
            self.register_bus(i2c)

        else:
            log.error("Invalid bus configuration: %s", bus_settings)

    def power_on(self):
        self.power_toggle_busses('power_on')
        self.power_toggle_sensors('power_on')

    def power_off(self):
        self.power_toggle_sensors('power_off')
        self.power_toggle_busses('power_off')

    def power_toggle_sensors(self, action):
        for sensor in self.sensors:
            sensorname = sensor.__class__.__name__
            if hasattr(sensor, action):
                log.info('Sending {} to sensor {}'.format(action, sensorname))
                try:
                    getattr(sensor, action)()
                except:
                    log.exception('Sending {} to sensor {} failed'.format(action, sensorname))

    def power_toggle_busses(self, action):
        for busname, bus in self.busses.items():
            if hasattr(bus, action):
                log.info('Sending {} to bus {}'.format(action, busname))
                try:
                    getattr(bus, action)()
                except:
                    log.exception('Sending {} to sensor {} failed'.format(action, busname))


class AbstractSensor:
    """
    Abstract sensor container, containing meta data as readings.
    """

    SENSOR_NOT_INITIALIZED = object()

    def __init__(self, settings=None):

        self.settings = settings or {}
        self.type = self.settings.get('type')

        self.name = None
        self.family = None
        self.driver = None

        """
        e.g. Multiple onewire sensors are address indexed on a bus.
        """
        self.address = None
        self.bus = None
        self.parameter = {}
        self.pins = {}

    def start(self):
        raise NotImplementedError("Must be implemented in sensor driver")

    def set_address(self, address):
        self.address = address

    def register_pin(self, name, pin):
        self.pins[name] = pin

    def register_parameter(self, name, parameter):
        self.parameter[name] = parameter

    def acquire_bus(self, bus):
        self.bus = bus

    def read(self):
        raise NotImplementedError()

    def format_fieldname(self, name, address):
        fieldname = '{name}.{address}.{bus}'.format(name=name, address=address, bus=self.bus.name)
        return fieldname

    def serialize(self):
        return dict(serialize_som(self.__dict__, stringify=['bus']))


class BusType:

    I2C = 'i2c'
    OneWire = 'onewire'


class AbstractBus:
    """
    A blueprint for all bus objects.
    """

    type = None

    def __init__(self, settings):
        """
        convention <type>:<index>
        """
        self.settings = settings
        self.number = self.settings['number']

        self.adapter = None
        # TODO: Publish found 1-Wire devices to MQTT bus and HTTP API.
        self.devices = []
        self.pins = {}

    @property
    def name(self):
        return str(self.type) + ":" + str(self.number)

    def register_pin(self, name, pin):
        self.pins[name] = pin

    def serialize(self):
        info = dict(serialize_som(self.__dict__))
        # FIXME: Why is that?
        info.update({'name': self.name, 'type': self.type})
        return info


class OneWireBus(AbstractBus):
    """
    Initialize the 1-Wire hardware driver and represent as bus object.
    """

    type = BusType.OneWire

    def start(self):
        # Todo: Improve error handling.
        try:
            from onewire.onewire import OneWire
            self.adapter = OneWire(Pin(self.pins['data']))
            self.scan_devices()

        except Exception as ex:
            log.exception('1-Wire hardware driver failed')

    def scan_devices(self):

        # Reset the 1-Wire device in case of leftovers.
        self.adapter.reset()

        # TODO: Tune this further?
        time.sleep(1)

        # Scan for 1-Wire devices and remember them.
        # TODO: Refactor things specific to DS18x20 devices elsewhere.
        self.devices = [rom for rom in self.adapter.scan() if rom[0] == 0x10 or rom[0] == 0x28]
        log.info("Found {} 1-Wire (DS18x20) devices: {}".format(len(self.devices), self.get_devices_ascii()))

    def get_devices_ascii(self):
        return list(map(self.device_address_ascii, self.devices))

    def serialize(self):
        info = super().serialize()
        if 'devices' in info:
            info['devices'] = self.get_devices_ascii()
        return info

    @staticmethod
    def device_address_ascii(address):
        # Compute ASCII representation of device address.
        if isinstance(address, (bytearray, bytes)):
            address = hexlify(address).decode()
        return address.lower()


class I2CBus(AbstractBus):
    """
    Initialize the I2C hardware driver and represent as bus object.
    """

    type = BusType.I2C

    def start(self):
        # Todo: Improve error handling.
        try:
            self.adapter = I2C(self.number, mode=I2C.MASTER, pins=(self.pins['sda'], self.pins['scl']), baudrate=100000)
            self.scan_devices()
        except Exception as ex:
            log.exception('I2C hardware driver failed')

    def scan_devices(self):
        self.devices = self.adapter.scan()
        # i2c.readfrom(0x76, 5)
        log.info("Found {} I2C devices: {}.".format(len(self.devices), self.devices))

    def power_off(self):
        """
        Turn off the I2C peripheral.

        https://docs.pycom.io/firmwareapi/pycom/machine/i2c.html
        """
        log.info('Turning off I2C bus {}'.format(self.name))
        self.adapter.deinit()


def serialize_som(thing, stringify=None):
    """
    Serialize the sensor object model to a representation
    suitable to be served for the device API.
    """
    stringify = stringify or []

    if isinstance(thing, list):
        hm = []
        for item in thing:
            hm.append(serialize_som(item))
        return hm

    elif isinstance(thing, dict):
        newthing = {}
        for key, value in thing.items():
            if key in stringify:
                newthing[key] = str(value)
            else:
                newthing[key] = serialize_som(value)
        return newthing

    elif isinstance(thing, (str, int, float, bool, set)) or type(thing) is type(None):
        return thing

    else:
        if hasattr(thing, 'serialize'):
            thing = thing.serialize()
        else:
            thing = str(thing)
        return thing
