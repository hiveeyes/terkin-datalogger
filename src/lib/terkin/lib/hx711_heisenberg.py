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

from terkin.lib.hx711 import HX711
from terkin import logging

log = logging.getLogger(__name__)


class HX711Heisenberg(HX711):
    """ """

    def __init__(self, dout, pd_sck, gain=128):
        super().__init__(dout, pd_sck, gain)

        self.time_constant = 0.9

    def read_median(self, times=10):
        """Acquire multiple readings and return median.

        :param times:  (Default value = 10)

        """
        lst = []
        # Fixme: Think about feeding the watchdog here.
        for i in range(times):
            lst.append(self.read())
        sortedLst = sorted(lst)
        #print(sortedLst)
        lstLen = len(lst)
        index = (lstLen - 1) // 2

        if (lstLen % 2):
            return sortedLst[index]
        else:
            return (sortedLst[index] + sortedLst[index + 1])/2.0

    def get_avgkg(self, times=3):
        """

        :param times:  (Default value = 3)

        """
        return round(self.get_value(times) / self.SCALE, 3)

    def get_lpkg(self):
        """ """
        self.filtered += self.time_constant * (self.read() - self.filtered)
        return round((self.filtered - self.OFFSET) / self.SCALE, 3)

    def get_reading(self):
        """ """
        value = self.read_median()
        reading = WeightReading(value, self.OFFSET, self.SCALE)
        return reading

    def tare(self, times=15):
        """

        :param times:  (Default value = 15)

        """
        sum = self.read_average(times)
        self.set_offset(sum)
        log.debug('OFFSET = ' + str(sum))

    def set_scale(self, scale=None):
        """

        :param scale:  (Default value = None)

        """
        if scale is None:
            return self.SCALE
        self.SCALE = scale

    def set_offset(self, offset=None):
        """

        :param offset:  (Default value = None)

        """
        if offset is None:
            return self.OFFSET
        self.OFFSET = offset


class WeightReading:
    """ """

    def __init__(self, rawvalue, offset, scale):
        self.raw = rawvalue
        self.offset = offset
        self.scale = scale
        #self.raw_short = None
        self.kg = None
        self.compute()

    def compute(self):
        """ """
        #self.raw_short = self.raw
        try:
            self.kg = round((self.raw - self.offset) / self.scale, 3)
        except Exception as ex:
            log.exc(ex, 'Computing kg value failed')

    def get_data(self):
        """ """
        return self.__dict__
