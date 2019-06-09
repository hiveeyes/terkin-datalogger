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

    def power_off(self):
        pass

    def power_on(self):
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


class OneWireBus(AbstractBus):
    # Initialize the OneWire hardware driver.

    type = BusType.OneWire

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

    type = BusType.I2C

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


class SystemMemoryFree:
    """
    Read free memory in bytes.
    """

    def read(self):
        import gc
        return {'system.memfree': gc.mem_free()}


class SystemTemperature:
    """
    Read the internal temperature of the MCU.

    - https://docs.micropython.org/en/latest/esp32/quickref.html#general-board-control
    - https://github.com/micropython/micropython-esp32/issues/33
    - https://github.com/micropython/micropython/pull/3933
    - https://github.com/micropython/micropython-esp32/pull/192
    - https://github.com/espressif/esp-idf/issues/146
    - https://forum.pycom.io/topic/2208/new-firmware-release-1-10-2-b1/4
    """

    def read(self):
        import machine
        temperature = machine.temperature()

        # Fahrenheit
        # 'system.temperature': 57.77778
        #temperature = (temperature - 32) / 1.8

        # Magic
        # 'system.temperature': 41.30435
        temperature = temperature * (44/23) + (-5034/23)

        reading = {'system.temperature': temperature}
        return reading


class SystemBatteryLevel:
    """
    Read the battery level by reading the ADC on a pin connected
    to a voltage divider, which is pin 16 on the expansion board.

    - https://docs.pycom.io/firmwareapi/pycom/machine/adc
    - https://docs.pycom.io/tutorials/all/adc
    - https://forum.pycom.io/topic/3776/adc-use-to-measure-battery-level-vin-level
    """
    def read(self):
        from machine import ADC
        adc = ADC()
        adc_channel = adc.channel(pin='P16', attn=ADC.ATTN_11DB)

        # Reads the channels value and converts it into a voltage (in millivolts).
        value = adc_channel.voltage() / 1000.0

        reading = {'system.voltage': value}
        return reading


class SystemHallSensor:
    """
    - https://forum.pycom.io/topic/3537/internal-hall-sensor-question/2
    - https://github.com/micropython/micropython-esp32/pull/211
    - https://www.esp32.com/viewtopic.php?t=481
    """
    pass


class SystemMemoryPeeker:
    """
    ``machine.mem32[]``
    - https://github.com/micropython/micropython-esp32/pull/192#issuecomment-334631994
    """
    pass


class ADC2:
    """
    ::

        adc = machine.ADC(machine.Pin(35))
        adc.atten(machine.ADC.ATTN_11DB)

    - https://github.com/micropython/micropython-esp32/issues/33
    - https://www.esp32.com/viewtopic.php?t=955
    """
    pass
