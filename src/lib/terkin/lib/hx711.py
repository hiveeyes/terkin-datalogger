# -*- coding: utf-8 -*-
# (c) 2017-2018 David Gerber <https://github.com/geda>
# HX711 library for the LoPy.
# https://github.com/geda/hx711-lopy
import utime
from terkin import logging
from machine import Pin, enable_irq, disable_irq, idle
from terkin.util import get_platform_info

log = logging.getLogger(__name__)


class HX711:
    """Baseline driver for the HX711 by David Gerber, with modifications.
    
    https://cdn.sparkfun.com/datasheets/Sensors/ForceFlex/hx711_english.pdf


    """

    def __init__(self, dout, pd_sck, gain=128):

        self.platform_info = get_platform_info()

        # Define two pins for clock and data.
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
            self.pSCK = Pin(int(pd_sck[1:]), mode=Pin.OUT)
            self.pOUT = Pin(int(dout[1:]), mode=Pin.IN, pull=Pin.PULL_UP)
        elif self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            self.pSCK = Pin(pd_sck, mode=Pin.OUT)
            self.pOUT = Pin(dout, mode=Pin.IN, pull=Pin.PULL_UP)
        else:
            raise NotImplementedError('HX711 is not implemented on this platform')

        self.initialized = False

        self.GAIN = 0
        self.OFFSET = 0
        self.SCALE = 1

        self.time_constant = 0.1
        self.filtered = None

        self.set_gain(gain)

    def set_gain(self, gain):
        """

        :param gain: 

        """
        if gain == 128:
            self.GAIN = 1
        elif gain == 64:
            self.GAIN = 3
        elif gain == 32:
            self.GAIN = 2

    def is_ready(self):
        """ """
        return self.pOUT() == 0

    def initialize(self):
        """Power and initialize the chip.
        Wait for becoming ready.


        """
        if not self.initialized:

            # Wake up the HX711.
            self.power_up()

            # Wait for device to become ready.
            log.info('Initialization started')
            self.wait_ready()
            self.initialized = True

            log.info('Initialization succeeded')
            return True

    def wait_ready(self):
        """ """
        retries = 10000
        #log.info('Waiting for device to become ready')
        while not self.is_ready():
            idle()
            retries -= 1
            if retries == 0:
                raise DeviceNotFound('HX711 not ready')
        #log.info('Device ready')

    def read(self):
        """This chip has a non-standard serial protocol.
        
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
        # Otherwise, croak with ``DeviceNotFound('HX711 not available')``.
        if not self.initialize():

            # Wait for the device becoming ready.
            self.wait_ready()

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
        """

        :param times:  (Default value = 3)

        """
        sum = 0
        for i in range(times):
            sum += self.read()
        return sum / times

    def read_lowpass(self):
        """ """
        if self.filtered is None:
            self.filtered = self.read()
        self.filtered += self.time_constant * (self.read() - self.filtered)
        return self.filtered

    def get_value(self, times=3):
        """

        :param times:  (Default value = 3)

        """
        return self.read_average(times) - self.OFFSET

    def get_units(self, times=3):
        """

        :param times:  (Default value = 3)

        """
        return self.get_value(times) / self.SCALE

    def tare(self, times=15):
        """

        :param times:  (Default value = 15)

        """
        sum = self.read_average(times)
        self.set_offset(sum)

    def set_scale(self, scale):
        """

        :param scale: 

        """
        self.SCALE = scale

    def set_offset(self, offset):
        """

        :param offset: 

        """
        self.OFFSET = offset

    def set_time_constant(self, time_constant = None):
        """

        :param time_constant:  (Default value = None)

        """
        if time_constant is None:
            return self.time_constant
        elif 0 < time_constant < 1.0:
            self.time_constant = time_constant

    def power_up(self):
        """When PD_SCK Input is low, chip is in normal working mode."""

        # Unfreeze pin hold when coming from deep sleep.
        # https://community.hiveeyes.org/t/strom-sparen-beim-einsatz-der-micropython-firmware-im-batteriebetrieb/2055/72
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            self.pSCK.hold(False)

        log.info('HX711 power up')
        self.pSCK.value(False)
        #utime.sleep_us(80)

        #self.initialize()

    def power_down(self):
        """When PD_SCK pin changes from low to high and stays at
        high for longer than 60µs, HX711 enters power down mode.


        """
        log.info('HX711 power down')
        state = disable_irq()
        self.pSCK.value(False)
        self.pSCK.value(True)
        utime.sleep_us(80)
        enable_irq(state)

        # Hold level to HIGH, even during deep sleep.
        # https://community.hiveeyes.org/t/strom-sparen-beim-einsatz-der-micropython-firmware-im-batteriebetrieb/2055/72
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            self.pSCK.hold(True)


class DeviceNotFound(Exception):
    """ """
    pass
