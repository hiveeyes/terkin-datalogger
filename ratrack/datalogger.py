# -*- coding: utf-8 -*-
#
# Ratrack MicroPython Datalogger
# https://github.com/hiveeyes/hiveeyes-micropython-firmware
#
# (c) 2019 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
from terkin.datalogger import TerkinDatalogger
from hiveeyes.sensor_bme280 import BME280Sensor
from hiveeyes.sensor_pytrack import PytrackSensor


class RatrackDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This time for MicroPython.
    """

    # Naming things.
    name = 'Ratrack MicroPython Datalogger'

    def register_sensors(self):
        """
        Add your sensors here.
        """

        # First, spin up the built-in sensors.
        super().register_sensors()

        # Add some project-specific sensors.
        self.device.tlog('Registering Ratrack sensors')

        # Setup the BME280.
        try:
            self.add_bme280_sensor()
        except Exception as ex:
            print('INFO:  Skipping bme280 sensor. {}'.format(ex))

        # Setup the Pytrack.
        try:
            self.add_pytrack_sensor()
        except Exception as ex:
            print('INFO:  Skipping Pytrack sensor. {}'.format(ex))

    def add_bme280_sensor(self):
        """
        Setup and register the DS18X20  sensor component with your data logger.
        """

        settings = self.settings.get('sensors.registry.bme280')
        bus = self.sensor_manager.get_bus_by_name(settings['bus'])

        sensor = BME280Sensor()
        sensor.acquire_bus(bus)

        # Start sensor.
        sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(sensor)

    def add_pytrack_sensor(self):
        """
        Setup and register the Pytrack sensor component with your data logger.
        """

        settings = self.settings.get('sensors.registry.pytrack')
        bus = self.sensor_manager.get_bus_by_name(settings['bus'])

        sensor = PytrackSensor()
        sensor.acquire_bus(bus)

        # Start sensor.
        sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(sensor)

    def loop(self):
        """
        Loop function. Do what I mean.
        """

        # It's your turn.
        #self.device.tlog('Ratrack loop')

        # Finally, schedule other system tasks.
        super().loop()
