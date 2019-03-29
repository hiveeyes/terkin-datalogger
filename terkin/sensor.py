# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3

from onewire.onewire import OneWire
from machine import Pin
from machine import I2C
from binascii import hexlify
import time

class SensorManager:
    def __init__(self):
        self.sensors = []
        self.busses = {}
        pass


    def register_sensor(self, sensor):
        self.sensors.append(sensor)

    def register_bus(self,  name, bus):
        print("INFO: registering bus: {}".format(name))
        self.busses[name] = bus
        pass

    def get_bus_by_name(self, name):
        return self.busses.get(name)

    def get_sensor_by_name(self, name):
       pass


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
        pass

    def register_pin(self, name, pin):
        self.pins[name] = pin

    def register_parameter(self, name, parameter):
        self.parameter[name] = parameter


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
        try:
            self.adapter = OneWire(Pin(self.pins['data']))
            self.scan_devices()
        except Exception as ex:
            print('ERROR: OneWire hardware driver failed. {}'.format(ex))
            raise


    def scan_devices(self):
        """
        resetting the OneWire device in case of leftovers
        """
        self.adapter.reset()
        time.sleep(0.750)
        """
        Scanning for OneWire devices and populate `devices`
        """
        self.devices = [rom for rom in self.adapter.scan() if rom[0] == 0x10 or rom[0] == 0x28]
        print("INFO:  Found {} OneWire (DS18x20) devices: {}.".format(len(self.devices), list(map(hexlify, self.devices))))


class I2CBus(AbstractBus):

    def start(self):
        try:
            self.adapter = I2C(self.bus_number, I2C.MASTER, baudrate=100000)
            self.scan_devices()
        except Exception as ex:
            print('ERROR: I2C hardware driver failed. {}'.format(ex))
            raise

    def scan_devices(self):
        self.devices = self.adapter.scan()
        print("INFO:  Found {} I2C devices: {}.".format(len(self.devices), self.devices))

    # print(i2c.scan())
    # print(i2c.readfrom(0x76, 5))


class MemoryFree:

    def read(self):
        import gc
        return {'memfree': gc.mem_free()}

