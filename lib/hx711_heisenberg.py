# -*- coding: utf-8 -*-
# (c) 2017-2018 David Gerber <https://github.com/geda>
# HX711 library for the LoPy.
# https://github.com/geda/hx711-lopy
"""
Updates
=======
(c) 2019 Ralf Lindlein <https://github.com/walterheisenberg>
License: GNU General Public License, Version 3
https://github.com/walterheisenberg/hivewatch_esp32/blob/master/lib/hx711lib.py

Setup
=====
::

    sc = HX711(0, 2)
    sc.set_scale(11.026667)
    sc.set_offset(130800.0)

    # Offset without wooden board
    #sc.set_offset(130748.3)

Notes
=====
- Some infos about low-pass filters
  https://microsoft.public.de.excel.narkive.com/PNakkyeu/tiefpassfilter

- The **time constant** means:

    - Lowers value will yield smoother low-pass filtering.
    - Use 0.9 to get more responsive values, 0.1 (default) means more filtered.

"""

from hx711 import HX711
from terkin import logging

log = logging.getLogger(__name__)


class HX711Heisenberg(HX711):

    def __init__(self, dout, pd_sck, gain=128):
        super().__init__(dout, pd_sck, gain)

        self.time_constant = 0.9

    def set_gain(self, gain):
        if gain is 128:
            self.GAIN = 1
        elif gain is 64:
            self.GAIN = 3
        elif gain is 32:
            self.GAIN = 2

        # v1: Skip first reading.
        #self.read()
        #self.filtered = self.read()

        # v2: Take average of three readings.
        # TODO: Maybe improve this.
        sum = 0
        for i in range(3):
            sum += self.read()
        self.filtered = sum / 3

        log.info('Gain & initial value set')

    def read_median(self, times=8):
        """
        Acquire multiple readings and return median.
        """
        lst = []
        for i in range(times):
            lst.append(self.read_average())
        sortedLst = sorted(lst)
        #print(sortedLst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2

        if (lstLen % 2):
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0

    def get_avgkg(self, times=3):
        return round(self.get_value(times) / self.SCALE / 1000, 3)

    def get_lpkg(self):
        self.filtered += self.time_constant * (self.read() - self.filtered)
        return round((self.filtered - self.OFFSET) / self.SCALE / 1000, 3)

    def get_medkg(self):
        return round((self.read_median() - self.OFFSET) / self.SCALE / 1000, 3)

    def tare(self, times=15):
        sum = self.read_average(times)
        self.set_offset(sum)
        log.debug('OFFSET = ' + str(sum))

    def set_scale(self, scale=None):
        if scale is None:
            return self.SCALE
        self.SCALE = scale

    def set_offset(self, offset=None):
        if offset is None:
            return self.OFFSET
        self.OFFSET = offset
