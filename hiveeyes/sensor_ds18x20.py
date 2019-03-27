# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3

import time
from onewire.onewire import DS18X20
from binascii import hexlify

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
        self.bus = None



    def acquire_bus(self, bus):
        self.bus = bus

    def start(self):
        if self.bus is None:
            raise KeyError("Bus missing")

        # Initialize the DS18x20 hardware driver.
        try:
            self.sensors = DS18X20(self.bus.adapter)
        except Exception as ex:
            print('ERROR: DS18X20 hardware driver failed. {}'.format(ex))
            raise




    def read(self):
        d = {}
        print('INFO:  Acquire reading from DS18X20')
        self.sensors.start_conversion()
        # for loop goes here
        for device in self.devices:
            time.sleep(1)
            value = self.sensors.read_temp_async(device)
            name = "temperature_" + hexlify(device).decode()
            d[name] = value

        return d
