# -*- coding: utf-8 -*-
# (c) 2016-2020 Clemens Gruber <clemens@hiveeyes.org>
# (c) 2017-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys
from terkin import logging
from terkin.sensor import SensorManager


log = logging.getLogger(__name__)


class ScaleAdjustment:
    """
    Python port of Open Hive scale adjustment sketch.

    https://github.com/hiveeyes/arduino/blob/master/scale-adjust/HX711/scale-adjust-hx711.ino
    """

    def __init__(self, sensor_manager: SensorManager):
        self.sensor_manager = sensor_manager

        # Sensor object of selected scale.
        self.sensor = None

        # Raw loadcell value when scale is unloaded.
        self.value_unloaded = None

        # Raw loadcell value when scale is loaded.
        self.value_loaded = None

        # Known weight put on the scale.
        self.adjustment_weight = None

    def start_wizard(self):
        self.cls()
        self.print_section('Weight scale adjustment', '=')
        self.select_sensor()
        self.start_sensor()
        self.read_unloaded()
        self.read_loaded()
        self.done()

    def select_sensor(self):
        while True:
            try:
                self.print_section('Step 1: Select sensor device')
                print()
                sensors = list(self.sensor_manager.get_sensors_by_family('scale'))
                for index, sensor in enumerate(sensors):
                    print('{}: {}'.format(index, sensor.settings.get('id')))
                print()
                sensor_index = int(input('Type index: '))
                self.sensor = sensors[sensor_index]
                print()
                break
            except KeyboardInterrupt:
                break
            except Exception as ex:
                log.exc(ex, 'Error while selecting sensor')

    def start_sensor(self):
        if hasattr(self.sensor, 'power_on'):
            self.sensor.power_on()
        if hasattr(self.sensor, 'loadcell') and hasattr(self.sensor.loadcell, 'initialize'):
            self.sensor.loadcell.initialize()

    def read_unloaded(self):
        while True:
            try:
                self.print_section('Step 2: Unloaded scale')
                print('Please remove all weight from the scale.')
                print('When done, press any key to continue.')
                self.wait_for_keypress()
                self.value_unloaded = float(self.sensor.loadcell.get_reading().raw)
                print()
                break
            except KeyboardInterrupt:
                break
            except Exception as ex:
                log.exc(ex, 'Error while reading unloaded scale')

    def read_loaded(self):
        while True:
            try:
                self.print_section('Step 3: Loaded scale')
                print('Please load the scale with a known weight.')
                print('When done, input the kilogram value.')
                print()

                self.adjustment_weight = float(input('Weight (kg): ').replace(',', '.'))
                self.value_loaded = float(self.sensor.loadcell.get_reading().raw)
                print()
                break
            except KeyboardInterrupt:
                break
            except Exception as ex:
                log.exc(ex, 'Error while reading loaded scale')

    def done(self):
        """
        Compute and output loadCellZeroOffset and loadCellKgDivider.
        """
        self.print_section('Step 4: Configure settings')
        print('Please use the computed values for configuring your settings.py')
        print()

        offset = self.value_unloaded
        divider = (self.value_loaded - self.value_unloaded) / self.adjustment_weight
        print('offset:', offset)
        print('scale: ', divider)

    def cls(self):
        sys.stdout.write(b"\x1b[2J")
        sys.stdout.write(b"\x1b[0;0H")

    def wait_for_keypress(self):
        sys.stdin.read(1)

    def print_section(self, message, char='-'):
        print()
        length = len(message)
        print(char * length)
        print(message)
        print(char * length)
