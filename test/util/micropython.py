# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys

from mock import Mock, MagicMock


def monkeypatch():
    monkeypatch_stdlib()
    monkeypatch_exceptions()
    monkeypatch_logging()
    monkeypatch_machine()
    monkeypatch_network()
    monkeypatch_hal()
    monkeypatch_pycom()


def monkeypatch_stdlib():

    import builtins
    builtins.const = int

    sys.modules['micropython'] = Mock()
    sys.modules['micropython'].const = int

    import struct
    sys.modules['ustruct'] = struct

    import binascii
    sys.modules['ubinascii'] = binascii

    import time
    def ticks_ms():
        import time
        return time.time_ns() / 1000000
    def ticks_diff(ticks1, ticks2):
        return abs(ticks1 - ticks2)
    time.ticks_ms = ticks_ms
    time.ticks_diff = ticks_diff
    sys.modules['utime'] = time

    import socket
    class socket_adapter(socket.socket):

        def write(self, data, length=None):
            if hasattr(data, 'encode'):
                data = data.encode()
            if length is not None:
                data = data[:length]
            return self.send(data)

        def read(self, length):
            return self.recv(length)

    sys.modules['usocket'] = socket
    sys.modules['usocket'].socket = socket_adapter

    import io
    sys.modules['uio'] = io

    import os
    sys.modules['uos'] = os

    import gc
    gc.threshold = Mock()
    gc.mem_free = Mock(return_value=1000000)
    gc.mem_alloc = Mock(return_value=2000000)

    # Optional convenience to improve speed.
    gc.collect = Mock()


def monkeypatch_exceptions():

    def print_exception(exc, file=sys.stdout):
        # file.write(str(exc))
        raise exc

    sys.print_exception = print_exception


def monkeypatch_machine():
    import uuid
    import machine

    # Some primitives.
    machine.enable_irq = Mock()
    machine.disable_irq = Mock()
    machine.unique_id = lambda: str(uuid.uuid4().fields[-1])[:5].encode()
    machine.freq = Mock(return_value=42000000)
    machine.idle = Mock()

    # Reset cause and wake reason.
    machine.PWRON_RESET = 0
    machine.HARD_RESET = 1
    machine.WDT_RESET = 2
    machine.DEEPSLEEP_RESET = 3
    machine.SOFT_RESET = 4
    machine.BROWN_OUT_RESET = 5

    machine.PWRON_WAKE = 0
    machine.GPIO_WAKE = 1
    machine.RTC_WAKE = 2
    machine.ULP_WAKE = 3

    machine.reset_cause = Mock(return_value=0)
    machine.wake_reason = wake_reason

    # 44.7053182608696°C
    machine.temperature = Mock(return_value=137.77778)

    # Pin class
    class PinPlus(machine.Pin):

        OPEN_DRAIN = 1999
        PULL_UP = 2999

        def init(self, mode=None, pull=None):
            pass

        def hold(self, enabled):
            pass

        def __call__(self, value=None):
            if value is None:
                return 0x00
                #for i in range(24):
                #    yield 0x00

    sys.modules['machine'].Pin = PinPlus

    class MockedI2C:
        """
        https://docs.pycom.io/firmwareapi/pycom/machine/i2c/
        """

        MASTER = 1

        def __init__(self, number, *args, **kwargs):

            # General
            self.number = number

            # Genuine
            self.mode = kwargs.get('mode')
            self.pins = kwargs.get('pins')
            self.baudrate = kwargs.get('baudrate')

            # Pycom
            self.sda = kwargs.get('sda')
            self.scl = kwargs.get('scl')
            self.freq = kwargs.get('freq')

        def readfrom_mem(self, addr, memaddr, nbytes, addrsize=8):
            result = None
            if addr in [0x76, 0x77]:

                # BME280 calibration for temperature and pressure.
                if memaddr == 0x88:
                    result = bytearray([
                                        # T1-3
                                        0x01, 0x02, 0x03, 0x04, 0xaa, 0x06,
                                        # P1-4
                                        0xff, 0x60, 0x01, 0x02, 0x00, 0x00, 0x00, 0x00,
                                        # P5-9
                                        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                                        # _, H1
                                        0x00, 0x00])

                # BME280 calibration for humidity.
                elif memaddr == 0xE1:
                    result = bytearray([0xff, 0x02, 0x00, 0x20, 0x00, 0x00, 0x00])

                # BME280_REGISTER_STATUS
                elif memaddr == 0xF3:
                    result = bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])

                # BME280 burst readout
                # TODO: Individualize this pre BME280 instance.
                elif memaddr == 0xF7:
                    result = bytearray([0x99, 0xbb, 0x03, 0x99, 0xee, 0xff, 0x99, 0xff])

            if result:
                return result
            else:
                raise KeyError('Unknown I2C memory address {} on device {}'.format(hex(memaddr), hex(addr)))

        def readfrom_mem_into(self, addr, memaddr, buf, addrsize=8):
            nbytes = len(buf)
            result = self.readfrom_mem(addr, memaddr, nbytes)
            buf.clear()
            for char in result:
                buf.append(char)

        def writeto_mem(self, addr, memaddr, buf, addrsize=8):
            pass

        def scan(self):
            return [0x76, 0x77]

    # I2C peripheral
    #machine.I2C = MagicMock()
    machine.I2C = MockedI2C

    # ADC peripheral
    machine.ADC = MagicMock()

    # UART peripheral
    machine.UART = MagicMock()


def wake_reason():
    from terkin.util import get_platform_info
    platform_info = get_platform_info()
    if platform_info.vendor == platform_info.MICROPYTHON.Pycom:
        return 0, None
    else:
        return 0


def monkeypatch_network():
    import network

    class MacAddresses:
        def __init__(self, sta_mac, ap_mac):
            self.sta_mac = sta_mac
            self.ap_mac = ap_mac

    class StationInfo:
        def __init__(self, ssid, sec):
            self.ssid = ssid
            self.sec = sec

    class WLANPlus(network.WLAN):

        STA = 1
        AP = 2
        STA_AP = 3

        def __init__(self, interface_id=None):
            super().__init__(interface_id)
            self._mode = None
            self._settings = {}

        # noinspection PyUnusedLocal
        def connect(self, ssid=None, password=None, *, bssid=None, timeout=None):
            self.is_connected_for_testing = True

        def init(self):
            pass

        def config(self, *args, **kwargs):

            if kwargs:
                self._settings.update(kwargs)

            else:

                param = args[0]

                if param == 'mac':
                    info = MacAddresses(sta_mac=self.get_local_mac(), ap_mac=self.get_local_mac(offset=1))
                    return info

                elif param == 'essid':
                    return 'FooBarWiFi'
                else:
                    raise KeyError('network.WLAN.config("{}") not mocked yet'.format(param))

        def ifconfig(self):
            info = ('192.168.42.42', '255.255.255.0', '192.168.42.1', '192.168.42.1')
            return info

        def mac(self):
            return self.get_local_mac()

        def mode(self, mode):
            self._mode = mode

        def ssid(self):
            return 'FooBarWiFi'

        def scan(self):
            return [StationInfo(ssid='FooBarWiFi', sec=3)]

        def status(self, param):
            if param == 'rssi':
                return -85.3

        @staticmethod
        def get_local_mac(offset=0):
            import uuid
            mac = uuid.getnode() + offset
            return mac.to_bytes(6, 'big')
            #return ':'.join(("%012x" % mac)[i:i + 2] for i in range(0, 12, 2))

    network.WLAN = WLANPlus


def monkeypatch_hal():

    class MockedOneWire:

        # TODO: Implement real conversation.

        def reset(self, pin):
            return True

        def writebyte(self, pin, value):
            #print('_onewire.writebyte({}, {})'.format(pin, hex(value)))
            pass

        def writebit(self, pin, value):
            pass

        def readbyte(self, pin):
            # 48.1875°C
            return 0x03

        def readbit(self, pin):
            return 0x00

        def crc8(self, data):
            # FIXME
            return 0

    #sys.modules['_onewire'] = MagicMock()
    sys.modules['_onewire'] = MockedOneWire()

    def onewire_scan(self):
        devices = [
            bytearray([0x28, 0xff, 0x64, 0x1d, 0x8f, 0xdf, 0x18, 0xc1]),
            bytearray([0x28, 0xff, 0x64, 0x1d, 0x8f, 0xc3, 0x94, 0x4f]),
        ]
        return devices

    import onewire_native
    sys.modules['onewire_native'].OneWire.scan = onewire_scan


def monkeypatch_pycom():

    import network
    network.Bluetooth = MagicMock()
    network.LTE = MagicMock()

    sys.modules['pycom'] = MagicMock()


def monkeypatch_logging():
    import io
    import logging

    def exc(self, e, msg, *args):
        buf = io.StringIO()
        sys.print_exception(e, buf)
        self.log(logging.ERROR, msg + "\n" + buf.getvalue(), *args)

    logging.Logger.exc = exc
