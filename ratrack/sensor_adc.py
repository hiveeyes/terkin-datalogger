# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import AbstractSensor

log = logging.getLogger(__name__)


class ADCSensor(AbstractSensor):

    def __init__(self):

        # Hardware parameters and configuration settings.

        super().__init__()

        # The driver instance.
        self.adc = None
        self.channel = None


    def start(self):
        try:
            from machine import ADC
            adc = ADC()
            self.channel = adc.channel(pin=self.pins['adc_in'], attn=ADC.ATTN_11DB)
            #p_out = Pin('P9', mode=Pin.OUT, pull=Pin.PULL_DOWN)

        except Exception as ex:
            log.exception('ADC hardware driver failed')
            raise

    def read_value(self):
        if self.channel is None:
            # TODO: Return Sensor.DISABLED
            return

        #log.info('Acquire reading from ADC')
        value = self.channel.value()

        return value


class MoistureSensor(ADCSensor):

    def read(self):
        value = self.read_value()
        data = {
            "moisture_raw": value,
            "moisture_volt": value / self.parameter.get('scaling', 4.096),
        }
        return data


class WaterlevelSensor(ADCSensor):

    def read(self):
        value = self.read_value()
        data = {
            "waterlevel_raw": value,
            "waterlevel_volt": value / self.parameter.get('scaling', 4.096),
        }
        return data
