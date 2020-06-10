# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys


def monkeypatch_cpython():

    # Setup logging.
    monkeypatch_logging()

    # Reconfigure other libraries.
    monkeypatch_stdlib()
    monkeypatch_exceptions()
    monkeypatch_machine()
    monkeypatch_pycom()


def monkeypatch_stdlib():

    from mock import Mock

    import time
    sys.modules['utime'] = time

    import builtins
    builtins.const = int

    import struct
    sys.modules['ustruct'] = struct

    import binascii
    sys.modules['ubinascii'] = binascii

    import time
    def ticks_ms():
        import time
        return time.time() * 1000
    def ticks_diff(ticks1, ticks2):
        return abs(ticks1 - ticks2)
    time.ticks_ms = ticks_ms
    time.ticks_diff = ticks_diff
    sys.modules['utime'] = time

    import io
    sys.modules['uio'] = io

    import os
    sys.modules['uos'] = os

    sys.modules['micropython'] = Mock()
    sys.modules['micropython'].const = int

    import gc
    gc.threshold = Mock()
    gc.mem_free = Mock(return_value=1000000)
    gc.mem_alloc = Mock(return_value=2000000)

    # Optional convenience to improve speed.
    gc.collect = Mock()


def monkeypatch_exceptions():

    import traceback

    def print_exception(exc, file=sys.stdout):
        traceback.print_exception(exc, exc, exc.__traceback__)

    sys.print_exception = print_exception


def monkeypatch_machine():

    from mock import Mock

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


def wake_reason():
    from terkin.util import get_platform_info
    platform_info = get_platform_info()
    if platform_info.vendor == platform_info.MICROPYTHON.Pycom:
        return 0, None
    else:
        return 0


def monkeypatch_pycom():

    from mock import MagicMock

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
