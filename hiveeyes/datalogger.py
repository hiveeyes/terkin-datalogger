# -*- coding: utf-8 -*-
#
# Hiveeyes MicroPython Datalogger
# https://github.com/hiveeyes/hiveeyes-micropython-firmware
#
# Conceived for the Bee Observer (BOB) project.
# https://community.hiveeyes.org/c/bee-observer
#
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
from terkin import logging
from terkin.datalogger import TerkinDatalogger
from hiveeyes.sensor_hx711 import HX711Sensor
from hiveeyes.sensor_ds18x20 import DS18X20Sensor
from hiveeyes.sensor_bme280 import BME280Sensor

log = logging.getLogger(__name__)


class HiveeyesDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This time for MicroPython.
    """

    # Naming things.
    name = 'Hiveeyes MicroPython Datalogger'

    def register_sensors(self):
        """
        Add your sensors here.
        """

        # First, spin up the built-in sensors.
        super().register_sensors()

        # Add some sensors for the Hiveeyes project.
        log.info('Registering Hiveeyes sensors')


        # Setup the HX711.
        try:
            self.add_hx711_sensor()
        except Exception as ex:
            log.exception('Setting up HX711 sensor failed')

        # Setup the DS18X20.
        try:
            self.add_ds18x20_sensor()
        except Exception as ex:
            log.exception('Setting up DS18X20 sensor failed')

        # Setup the BME280.
        try:
            self.add_bme280_sensor()
        except Exception as ex:
            log.exception('Setting up BME280 sensor failed')

    def add_hx711_sensor(self):
        """
        Setup and register the HX711 sensor component with your data logger.
        """

        # Initialize HX711 sensor component.
        settings = self.settings.get('sensors.registry.hx711')

        if settings.get('enabled') is False:
            log.info("Skipping HX711 device on pins {}/{}".format(settings['pin_dout'], settings['pin_pdsck']))
            return

        hx711_sensor = HX711Sensor()
        hx711_sensor.set_address(settings.get('address', 0x00))
        hx711_sensor.register_pin('dout', settings['pin_dout'])
        hx711_sensor.register_pin('pdsck', settings['pin_pdsck'])
        hx711_sensor.register_parameter('scale', settings['scale'])
        hx711_sensor.register_parameter('offset', settings['offset'])
        hx711_sensor.register_parameter('gain', settings.get('gain', 128))
        hx711_sensor.select_driver('heisenberg')

        # Select driver module. Use "gerber" (vanilla) or "heisenberg" (extended).

        # Start sensor.
        hx711_sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(hx711_sensor)

    def add_ds18x20_sensor(self):
        """
        Setup and register the DS18X20  sensor component with your data logger.
        """

        settings = self.settings.get('sensors.registry.ds18x20')

        bus = self.sensor_manager.get_bus_by_name(settings['bus'])
        sensor = DS18X20Sensor(settings=settings)
        sensor.acquire_bus(bus)

        # Start sensor.
        sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(sensor)

    def add_bme280_sensor(self):
        """
        Setup and register the DS18X20  sensor component with your data logger.
        """

        settings = self.settings.get('sensors.registry.bme280')
        bus = self.sensor_manager.get_bus_by_name(settings['bus'])

        if settings.get('enabled') is False:
            log.info("Skipping BME280 device {} on bus {}".format(hex(settings['address']), bus.name))
            return

        sensor = BME280Sensor()
        if 'address' in settings:
            sensor.set_address(settings['address'])
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
        #log.info('Hiveeyes loop')

        # Finally, schedule other system tasks.
        super().loop()
