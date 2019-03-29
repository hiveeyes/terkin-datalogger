# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from binascii import hexlify
from machine import Pin
from machine import I2C
from terkin import logging

log = logging.getLogger(__name__)


class SensorManager:

    def __init__(self):
        self.sensors = []
        self.busses = {}

    def register_sensor(self, sensor):
        self.sensors.append(sensor)

    def register_bus(self,  name, bus):
        log.info('Registering bus "%s"', name)
        self.busses[name] = bus

    def get_bus_by_name(self, name):
        return self.busses.get(name)

    def get_sensor_by_name(self, name):
        raise NotImplementedError('"get_sensor_by_name" not implemented yet')


class AbstractBus:
    def __init__(self, bus_number):
        """
        convention <type>:<index>
        """
        self.name = None
        self.adapter = None
        self.devices = []
        self.pins = {}
        self.bus_number = bus_number

    def register_pin(self, name, pin):
        self.pins[name] = pin


class AbstractSensor:
    """
    Abstract sensor container, containing meta data as readings
    """

    SENSOR_NOT_INITIALIZED = object()

    def __init__(self):
        self.name = None
        self.family = None
        self.driver = None

        """
        e.g. multiple onewire sensors are address indexed on a bus.
        """
        self.address = None
        self.bus = None
        self.parameter = {}
        self.pins = {}

    def start(self):
        raise NotImplementedError("Must be implemented in sensor driver")

    def register_pin(self, name, pin):
        self.pins[name] = pin

    def register_parameter(self, name, parameter):
        self.parameter[name] = parameter

    def acquire_bus(self, bus):
        self.bus = bus

    def power_off(self):
        pass

    def power_on(self):
        pass

    def read(self):
        raise NotImplementedError()
        pass


class OneWireBus(AbstractBus):
    # Initialize the OneWire hardware driver.

    def start(self):
        # TODO: Improve error handling.
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

    def start(self):
        # TODO: Improve error handling.
        try:
            self.adapter = I2C(self.bus_number, mode=I2C.MASTER, pins=(self.pins['sda'], self.pins['scl']), baudrate=100000)
            self.scan_devices()
        except Exception as ex:
            log.exception('I2C hardware driver failed')

    def scan_devices(self):
        self.devices = self.adapter.scan()
        # i2c.readfrom(0x76, 5)
        log.info("Found {} I2C devices: {}.".format(len(self.devices), self.devices))


class MemoryFree:

    def read(self):
        import gc
        return {'memfree': gc.mem_free()}
