# -*- coding: utf-8 -*-
# (c) 2017-2018 David Gerber <https://github.com/geda>
# HX711 library for the LoPy.
# https://github.com/geda/hx711-lopy
from terkin import logging
from machine import Pin, enable_irq, disable_irq, idle

log = logging.getLogger(__name__)


class HX711:
    """
    Baseline driver for the HX711 by David Gerber, with modifications.

    https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf
    """

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
        """
        This chip has a non-standard serial protocol.

        Serial Interface
        ----------------
        Pin PD_SCK and DOUT are used for data retrieval, input selection,
        gain selection and power down controls.

        When output data is not ready for retrieval, digital output pin DOUT
        is high. Serial clock input PD_SCK should be low. When DOUT goes to
        low, it indicates data is ready for retrieval.

        By applying 25~27 positive clock pulses at the PD_SCK pin, data is
        shifted out from the DOUT output pin. Each PD_SCK pulse shifts out
        one bit, starting with the MSB bit first, until all 24 bits are
        shifted out. The 25th pulse at PD_SCK input will pull DOUT pin back
        to high.
        """

        # Initialize the hardware once.
        if self.initialize() is False:
            raise DeviceNotFound('HX711 not available')

        # Wait for the device being ready.
        # FIXME: This might block forever?
        while not self.is_ready():
            idle()

        # Shift in data, gain & channel info.
        result = 0
        for j in range(24 + self.GAIN):
            state = disable_irq()
            self.pSCK(True)
            self.pSCK(False)
            result = (result << 1) | self.pOUT()
            enable_irq(state)

        # Shift back the extra bits.
        result >>= self.GAIN

        # Check sign.
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
        log.info('HX711 power down')
        state = disable_irq()
        self.pSCK.value(False)
        self.pSCK.value(True)
        enable_irq(state)

    def power_up(self):
        log.info('HX711 power up')
        self.pSCK.value(False)


class DeviceNotFound(Exception):
    pass
