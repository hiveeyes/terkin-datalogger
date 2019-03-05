import os

import machine
from machine import Timer
from ubinascii import hexlify


class Application:

    def __init__(self, name, version):

        self.name = name
        self.version = version

        # Keep track of time since boot.
        self.chrono = Timer.Chrono()
        self.chrono.start()

    def enable_serial(self):
        # Disable these two lines if you don't want serial access.
        uart = machine.UART(0, 115200)
        os.dupterm(uart)

    def elapsed(self):
        return self.chrono.read()

    def tlog(self, message):
        now = self.elapsed()
        print('[{}] {}'.format(now, message))

    def print_bootscreen(self):

        # Print startup screen.
        title = '{} {}'.format(self.name, self.version)
        print('=' * len(title))
        print(title)
        print('=' * len(title))
        print('CPU freq     {} MHz'.format(machine.freq() / 1000000))
        print('Device id    {}'.format(hexlify(machine.unique_id())))
        print()
        machine.info()
        print()
