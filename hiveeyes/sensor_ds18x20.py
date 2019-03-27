# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3

import time
from machine import Pin
from onewire.onewire import DS18X20
from onewire.onewire import OneWire

from terkin.sensor import AbstractSensor

"""
# DS18B20 data line connected to pin P10

while True:
    print(temp.read_temp_async())
    time.sleep(1)
    temp.start_conversion()
    time.sleep(1)

"""

class DS18X20Sensor(AbstractSensor):
    """
    A generic DS18B20 sensor component.
    """


    def __init__(self):
        super().__init__()

        # The driver instance.
        self.wire = None
        self.devices = []
        self.readings = None
        self.sensors = None


    def start(self):

        # Initialize the OneWire hardware driver.
        try:
            self.wire = OneWire(Pin(self.pins['data']))
        except Exception as ex:
            print('ERROR: OneWire hardware driver failed. {}'.format(ex))
            raise

        # Initialize the DS18x20 hardware driver.
        try:
            self.sensors = DS18X20(self.wire)
        except Exception as ex:
            print('ERROR: DS18X20 hardware driver failed. {}'.format(ex))
            raise

        #self.scan_devices()


    def scan_devices(self):
        self.devices = self.sensors.scan()
        print(self.devices)


    def read(self):

        # device = self.devices[0]

        print('INFO:  Acquire reading from DS18X20')
        self.sensors.start_conversion()
        time.sleep_ms(750)
        # for loop goes here
        value = self.sensors.read_temp_async()
        return {'temperature': value}
