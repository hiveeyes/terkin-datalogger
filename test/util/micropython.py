import sys

from mock import Mock, MagicMock

from terkin.util import get_platform_info


def monkeypatch():
    monkeypatch_stdlib()
    monkeypatch_logging()
    monkeypatch_machine()
    monkeypatch_network()
    monkeypatch_pycom()


def monkeypatch_stdlib():

    import builtins
    builtins.const = int

    import struct
    sys.modules['ustruct'] = struct

    import binascii
    sys.modules['ubinascii'] = binascii

    sys.print_exception = print_exception

    import time
    time.ticks_ms = ticks_ms
    time.ticks_diff = ticks_diff
    sys.modules['utime'] = time

    import gc
    gc.threshold = Mock()


def monkeypatch_machine():
    import uuid
    import machine
    machine.I2C = MagicMock()
    machine.enable_irq = Mock()
    machine.disable_irq = Mock()
    machine.unique_id = lambda: str(uuid.uuid4().fields[-1])[:5].encode()
    machine.freq = Mock()
    machine.freq.return_value = 42000000
    machine.idle = Mock()

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

    machine.reset_cause = Mock()
    machine.reset_cause.return_value = 0
    machine.wake_reason = wake_reason


def wake_reason():
    platform_info = get_platform_info()
    if platform_info.vendor == platform_info.MICROPYTHON.Vanilla:
        return 0
    else:
        return 0, None


def monkeypatch_network():
    import network

    class MacAddresses:
        def __init__(self, sta_mac, ap_mac):
            self.sta_mac = sta_mac
            self.ap_mac = ap_mac

    class WLANPlus(network.WLAN):

        def config(self, param):

            if param == 'mac':
                info = MacAddresses(sta_mac=self.get_local_mac(), ap_mac=self.get_local_mac(offset=1))
                return info

            elif param == 'essid':
                return 'ExampleWiFiNetwork'
            else:
                raise KeyError('network.WLAN.config("{}") not mocked yet'.format(param))

        def ifconfig(self):
            info = ('192.168.42.42', '255.255.255.0', '192.168.42.1', '192.168.42.1')
            return info

        @staticmethod
        def get_local_mac(offset=0):
            import uuid
            mac = uuid.getnode() + offset
            return mac.to_bytes(6, 'big')
            #return ':'.join(("%012x" % mac)[i:i + 2] for i in range(0, 12, 2))

    network.WLAN = WLANPlus


def monkeypatch_pycom():

    import network
    network.Bluetooth = MagicMock()

    import test.util.pycom
    sys.modules['pycom'] = test.util.pycom


def monkeypatch_logging():
    import logging
    import io
    def exc(self, e, msg, *args):
        buf = io.StringIO()
        sys.print_exception(e, buf)
        self.log(logging.ERROR, msg + "\n" + buf.getvalue(), *args)

    logging.Logger.exc = exc


# Utility functions.

def print_exception(exc, file=sys.stdout):
    #file.write(str(exc))
    raise exc


def ticks_ms():
    import time
    return time.time_ns() / 1000


def ticks_diff(ticks1, ticks2):
    return abs(ticks1 - ticks2)
