# -*- coding: utf-8 -*-
# (c) 2017-2018 David Gerber <https://github.com/geda>
# HX711 library for the LoPy.
# https://github.com/geda/hx711-lopy
from terkin import logging
from machine import Pin, enable_irq, disable_irq, idle

log = logging.getLogger(__name__)


class HX711:
    def __init__(self, dout, pd_sck, gain=128):

        self.pSCK = Pin(pd_sck, mode=Pin.OUT)
        self.pOUT = Pin(dout, mode=Pin.IN, pull=Pin.PULL_DOWN)
        self.pSCK.value(False)

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1

        self.time_constant = 0.1
        self.filtered = 0

        self.initialized = False

        self.set_gain(gain)

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

    def is_ready(self):
        return self.pOUT() == 0

    def initialize(self):
        """To initialize the chip, perform an initial reading once"""
        if not self.initialized:
            log.info('HX711 initialization started')
            if self.is_ready():
                self.initialized = True

                # FIXME: These two functions have been moved
                #        here from the ``set_gain()`` method.
                #        Are they actually required?
                self.read()
                self.filtered = self.read()

                log.info('HX711 initialization succeeded')
                return True
            else:
                log.error('HX711 not found, skipping initialization')
                return False

    def read(self):

        # Initialize the hardware once.
        if self.initialize() is False:
            # TODO: HardwareNotFoundError
            raise KeyError('HX711 not available')

        # wait for the device being ready
        while not self.is_ready():
            idle()

        # shift in data, and gain & channel info
        result = 0
        for j in range(24 + self.GAIN):
            state = disable_irq()
            self.pSCK(True)
            self.pSCK(False)
            enable_irq(state)
            result = (result << 1) | self.pOUT()

        # shift back the extra bits
        result >>= self.GAIN

        # check sign
        if result > 0x7fffff:
            result -= 0x1000000

        return result

    def read_average(self, times=3):
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def read_lowpass(self):
        self.filtered += self.time_constant * (self.read() - self.filtered)
        return self.filtered

    def get_value(self, times=3):
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        self.SCALE = scale

    def set_offset(self, offset):
        self.OFFSET = offset

    def set_time_constant(self, time_constant = None):
        if time_constant is None:
            return self.time_constant
        elif 0 < time_constant < 1.0:
            self.time_constant = time_constant

    def power_down(self):
        self.pSCK.value(False)
        self.pSCK.value(True)

    def power_up(self):
        self.pSCK.value(False)
