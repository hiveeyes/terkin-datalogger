# -*- coding: utf-8 -*-
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2019-2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# License: GNU General Public License, Version 3
from binascii import hexlify
from machine import Pin

from terkin import logging
from terkin.sensor.common import AbstractBus

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)


class BusType:
    """  """

    I2C = 'i2c'
    OneWire = 'onewire'


class SensorManager:
    """Manages all buses and sensors."""

    def __init__(self, settings):
        self.sensors = []
        self.buses = {}
        self.settings = settings

    def register_sensor(self, sensor):
        """

        :param sensor: 

        """
        self.sensors.append(sensor)

    def register_bus(self,  bus):
        """

        :param bus: 

        """
        bus_name = bus.name
        log.info('Registering bus "%s"', bus_name)
        self.buses[bus_name] = bus

    def get_bus_by_name(self, name):
        """

        :param name: 

        """
        if name is None:
            log.error('Bus "{}" does not exist'.format(name))
            return

        log.debug('Trying to find bus by name "%s"', name)
        bus = self.buses.get(name)
        log.debug('Found bus by name "%s": %s', name, bus)
        return bus

    def get_sensor_by_name(self, name):
        """

        :param name: 

        """
        raise NotImplementedError('"get_sensor_by_name" not implemented yet')

    def get_sensors_by_family(self, family):
        """
        Return all sensors filtered by family.
        """
        for sensor in self.sensors:
            if hasattr(sensor, 'family') and sensor.family == family:
                yield sensor

    def setup_buses(self, buses_settings):
        """Register configured I2C, OneWire and SPI buses.

        :param buses_settings: 

        """

        effective_buses = []
        effective_bus_ids = []
        for bus_settings in buses_settings:

            if bus_settings.get("enabled"):
                effective_buses.append(bus_settings)
                effective_bus_ids.append(bus_settings['id'])

        log.info('Starting buses: %s', effective_bus_ids)

        for bus_settings in effective_buses:
            try:
                self.setup_bus(bus_settings)
            except Exception as ex:
                log.exc(ex, 'Registering bus failed. settings={}'.format(bus_settings))

    def setup_bus(self, bus_settings):
        """

        :param bus_settings:

        """
        bus_family = bus_settings.get('family')

        if bus_family == BusType.OneWire:
            owb = OneWireBus(bus_settings)
            if 'pin_data' in bus_settings:
                owb.register_pin("data", bus_settings['pin_data'])
            owb.start()
            self.register_bus(owb)

        elif bus_family == BusType.I2C:
            i2c = I2CBus(bus_settings)
            if 'pin_sda' in bus_settings:
                i2c.register_pin("sda", bus_settings['pin_sda'])
            if 'pin_scl' in bus_settings:
                i2c.register_pin("scl", bus_settings['pin_scl'])
            i2c.start()
            self.register_bus(i2c)

        else:
            log.error("Invalid bus configuration: %s", bus_settings)

    def power_on(self):
        """Send power-on to all buses and sensors"""
        if self.settings.get('sensors.power_toggle_buses', True):
            self.power_toggle_buses('power_on')
        if self.settings.get('sensors.power_toggle_sensors', True):
            self.power_toggle_sensors('power_on')

    def power_off(self):
        """Send power-off to all buses and sensors"""
        if self.settings.get('sensors.power_toggle_sensors', True):
            self.power_toggle_sensors('power_off')
        if self.settings.get('sensors.power_toggle_buses', True):
            self.power_toggle_buses('power_off')

    def power_toggle_sensors(self, action):
        """

        :param action:

        """
        for sensor in self.sensors:
            sensorname = sensor.__class__.__name__
            if hasattr(sensor, action):
                log.info('Sending {} to sensor {}'.format(action, sensorname))
                try:
                    getattr(sensor, action)()
                except Exception as ex:
                    log.exc(ex, 'Sending {} to sensor {} failed'.format(action, sensorname))

    def power_toggle_buses(self, action):
        """

        :param action:

        """
        for busname, bus in self.buses.items():
            if hasattr(bus, action):
                log.info('Sending {} to bus {}'.format(action, busname))
                try:
                    getattr(bus, action)()
                except Exception as ex:
                    log.exc(ex, 'Sending {} to sensor {} failed'.format(action, busname))

    def start_sensors(self):
        log.info("Starting all sensors")
        for sensor in self.sensors:
            if hasattr(sensor, 'start'):
                try:
                    sensor.start()
                except Exception as ex:
                    log.exc(ex, 'Starting sensor "{}" failed. Reason: {}.'.format(sensor.type, ex))


class OneWireBus(AbstractBus):
    """Initialize the 1-Wire hardware driver and represent as bus object."""

    type = BusType.OneWire

    def start(self):
        """  """
        # Todo: Improve error handling.
        try:

            # Vanilla MicroPython 1.11
            if self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
                pin = Pin(int(self.pins['data'][1:]))
                import onewire_native
                self.adapter = onewire_native.OneWire(pin)

            # Pycom MicroPython 1.9.4
            elif self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
                pin = Pin(self.pins['data'])
                if self.settings.get('driver') == 'native':
                    log.info('Using native 1-Wire driver on Pycom MicroPython')
                    import onewire_native
                    self.adapter = onewire_native.OneWire(pin)
                else:
                    log.info('Using pure-Python 1-Wire driver on Pycom MicroPython')
                    import onewire_python
                    self.adapter = onewire_python.OneWire(pin)

            elif self.platform_info.vendor == self.platform_info.MICROPYTHON.RaspberryPi:
                from terkin.sensor.linux import LinuxSysfsOneWireBus
                sysfs = self.settings['sysfs']
                self.adapter = LinuxSysfsOneWireBus(sysfs)

            else:
                raise NotImplementedError('1-Wire bus support is not implemented on this platform')

            self.scan_devices()
            self.ready = True

        except Exception as ex:
            #log.exc(ex, '1-Wire hardware driver failed')
            #return False
            raise

        return True

    def scan_devices(self):
        """  """

        # The 1-Wire bus sometimes needs a fix when coming back from deep sleep.
        #self.adapter.reset()

        # TODO: Tune this further?
        #time.sleep(1)

        # Scan for 1-Wire devices and remember them.
        # TODO: Refactor things specific to DS18x20 devices elsewhere.
        self.devices = [rom for rom in self.adapter.scan() if rom[0] == 0x10 or rom[0] == 0x28]
        log.info("Found {} 1-Wire (DS18x20) devices: {}".format(len(self.devices), self.get_devices_ascii()))

    def get_devices_ascii(self):
        """  """
        return list(map(self.device_address_ascii, self.devices))

    def serialize(self):
        """  """
        info = super().serialize()
        if 'devices' in info:
            info['devices'] = self.get_devices_ascii()
        return info

    @staticmethod
    def device_address_ascii(address):
        """

        :param address:

        """
        # Compute ASCII representation of device address.
        if isinstance(address, (bytearray, bytes)):
            address = hexlify(address).decode()
        return address.lower()


class I2CBus(AbstractBus):
    """Initialize the I2C hardware driver and represent as bus object."""

    type = BusType.I2C
    frequency = 100000

    def start(self):
        """  """
        # Todo: Improve error handling.
        try:
            if self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
                from machine import I2C
                self.adapter = I2C(self.number, sda=Pin(int(self.pins['sda'][1:])), scl=Pin(int(self.pins['scl'][1:])), freq=self.frequency)

            elif self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
                from machine import I2C
                self.adapter = I2C(self.number, mode=I2C.MASTER, pins=(self.pins['sda'], self.pins['scl']), baudrate=self.frequency)

            elif self.platform_info.vendor == self.platform_info.MICROPYTHON.Odroid:
                from smbus2 import SMBus
                self.adapter = SMBus(self.number)

            elif self.platform_info.vendor == self.platform_info.MICROPYTHON.RaspberryPi:
                import board
                import busio

                def i2c_add_bus(busnum, scl, sda):
                    """
                    Register more I2C buses with Adafruit Blinka.

                    Make Adafruit Blinka learn another I2C bus.
                    Please make sure you define it within /boot/config.txt like::

                    dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=26,i2c_gpio_scl=20
                    """

                    # Uncache this module, otherwise monkeypatching will fail on subsequent calls.
                    import sys
                    try:
                        del sys.modules['microcontroller.pin']
                    except:
                        pass

                    # Monkeypatch "board.pin.i2cPorts".
                    i2c_port = (busnum, scl, sda)
                    if i2c_port not in board.pin.i2cPorts:
                        board.pin.i2cPorts += (i2c_port,)

                pin_scl = self.pins['scl']
                pin_sda = self.pins['sda']

                # When I2C port pins are defined as Integers, register them first.
                if isinstance(pin_scl, int):
                    i2c_add_bus(self.number, pin_scl, pin_sda)
                    SCL = board.pin.Pin(pin_scl)
                    SDA = board.pin.Pin(pin_sda)

                # When I2C port pins are defined as Strings and start with "board.",
                # they are probably already Pin aliases of Adafruit Blinka.
                elif isinstance(pin_scl, str) and pin_scl.startswith('board.'):
                    SCL = eval(pin_scl)
                    SDA = eval(pin_sda)

                self.adapter = busio.I2C(SCL, SDA)

            else:
                raise NotImplementedError('I2C bus is not implemented on this platform')

            self.just_started = True

            if not self.platform_info.vendor == self.platform_info.MICROPYTHON.Odroid:
                self.scan_devices()

            if self.platform_info.vendor == self.platform_info.MICROPYTHON.Odroid:

                self.devices = self.scan_devices_smbus2()
                log.info("Scan I2C bus via smbus2 for devices...")
                log.info("Found {} I2C devices: {}.".format(len(self.devices), self.devices))

            self.ready = True

        except Exception as ex:
            #log.exc(ex, 'I2C hardware driver failed')
            raise

    def scan_devices(self):
        log.info('Scan I2C with id={} bus for devices...'.format(self.number))
        self.devices = self.adapter.scan()
        # i2c.readfrom(0x76, 5)
        log.info("Found {} I2C devices: {}".format(len(self.devices), self.devices))

    def scan_devices_smbus2(self, start=0x03, end=0x78):
        try:
            list = []
            for i in range(start, end):
                val = 1
                try:
                    self.adapter.read_byte(i)
                except OSError as e:
                    val = e.args[0]
                finally:
                    if val != 5:  # No device
                        if val == 1:
                            res = "Available"
                        elif val == 16:
                            res = "Busy"
                        elif val == 110:
                            res = "Timeout"
                        else:
                            res = "Error code: " + str(val)
                        # print(hex(i) + " -> " + res)
                        if res == 'Available':
                            # print(i)
                            list.append(i)
            return list

        except Exception as exp:
            log.exc(exp, 'scan smbus2 failed')

    def power_on(self):
        """
        Turn on the I2C peripheral after power off.
        """

        # Don't reinitialize device if power on just occurred through initial driver setup.
        if self.just_started:
            self.just_started = False
            return

        # uPy doesn't have deinit so it doesn't need init
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            from machine import I2C
            self.adapter.init(mode=I2C.MASTER, baudrate=self.frequency)

    def power_off(self):
        """
        Turn off the I2C peripheral.

        https://docs.pycom.io/firmwareapi/pycom/machine/i2c.html
        """
        log.info('Turning off I2C bus {}'.format(self.name))
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            self.adapter.deinit()
