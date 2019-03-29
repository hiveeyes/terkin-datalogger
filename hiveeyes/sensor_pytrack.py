# -*- coding: utf-8 -*-
# (c) 2019 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin.sensor import AbstractSensor


class PytrackSensor(AbstractSensor):
    """
    A Pytrack sensor component.
    """

    def __init__(self):
        super().__init__()

        # The driver instance.
        self.readings = None
        self.sensor = None
        self.bus = None

    def start(self):
        """
        Getting the bus
        """
        if self.bus is None:
            raise KeyError("I2C bus missing")

        # Initialize the hardware driver.
        try:
            from pytrack import Pytrack
            self.sensor = Pytrack(i2c=self.bus.adapter)
        except Exception as ex:
            print('ERROR: Pytrack hardware driver failed. {}'.format(ex))
            raise

    def read(self):
        data = {}
        print('INFO:  Acquire reading from Pytrack')
        data['battery_voltage'] = float(self.sensor.read_battery_voltage())
        print("Pytrack data: {}".format(data))
        return data
