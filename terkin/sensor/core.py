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

    def register_busses(self, bus_settings):
        """
        Register configured I2C, OneWire and SPI busses.
        """
        log.info("Starting all busses %s", bus_settings)
        for bus in bus_settings:
            if not bus.get("enabled", False):
                continue
            if bus['family'] == BusType.OneWire:
                owb = OneWireBus(bus["number"])
                owb.register_pin("data", bus['pin_data'])
                owb.start()
                self.register_bus(owb)

            elif bus['family'] == BusType.I2C:
                i2c = I2CBus(bus["number"])
                i2c.register_pin("sda", bus['pin_sda'])
                i2c.register_pin("scl", bus['pin_scl'])
                i2c.start()
                self.register_bus(i2c)

            else:
                log.warning("Invalid bus configuration: %s", bus)

    def power_off(self):
        for sensor in self.sensors:
            if hasattr(sensor, 'power_off'):
                try:
                    sensor.power_off()
                except:
                    log.exception('Turning off sensor failed')

        for busname, bus in self.busses.items():
            if hasattr(bus, 'power_off'):
                bus.power_off()


class AbstractSensor:
    """
    Abstract sensor container, containing meta data as readings.
    """

    SENSOR_NOT_INITIALIZED = object()

    def __init__(self):
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

    def power_on(self):
        pass

    def power_off(self):
        pass

    def read(self):
        raise NotImplementedError()
        pass

    def format_fieldname(self, name, address):
        fieldname = '{name}.{address}.{bus}'.format(name=name, address=address, bus=self.bus.name)
        return fieldname


class BusType:

    I2C = 'i2c'
    OneWire = 'onewire'


class AbstractBus:
    """
    A blueprint for all bus objects.
    """

    type = None

    def __init__(self, bus_number):
        """
        convention <type>:<index>
        """
        self.adapter = None
        self.devices = []
        self.pins = {}
        self.bus_number = bus_number

    @property
    def name(self):
        return str(self.type) + ":" + str(self.bus_number)

    def register_pin(self, name, pin):
        self.pins[name] = pin

    def power_on(self):
        pass

    def power_off(self):
        pass


class OneWireBus(AbstractBus):
    """
    Initialize the OneWire hardware driver and represent as bus object.
    """

    type = BusType.OneWire

    def start(self):
        # Todo: Improve error handling.
        try:
            from onewire.onewire import OneWire
            self.adapter = OneWire(Pin(self.pins['data']))
            self.scan_devices()
        except Exception as ex:
            log.exception('OneWire hardware driver failed')

    def scan_devices(self):
        """
        Resetting the OneWire device in case of leftovers
        """
        self.adapter.reset()
        time.sleep(0.750)
        # Scan for OneWire devices and populate `devices`.
        self.devices = [rom for rom in self.adapter.scan() if rom[0] == 0x10 or rom[0] == 0x28]
        log.info("Found {} OneWire (DS18x20) devices: {}.".format(len(self.devices), list(map(hexlify, self.devices))))


class I2CBus(AbstractBus):
    """
    Initialize the I2C hardware driver and represent as bus object.
    """

    type = BusType.I2C

    def start(self):
        # Todo: Improve error handling.
        try:
            self.adapter = I2C(self.bus_number, mode=I2C.MASTER, pins=(self.pins['sda'], self.pins['scl']), baudrate=100000)
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
