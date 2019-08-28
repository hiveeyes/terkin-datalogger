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

log = logging.getLogger(__name__)


class HiveeyesDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This time for MicroPython.
    """

    # Naming things.
    name = 'Hiveeyes MicroPython Datalogger'

    def setup(self):
        super().setup()

    def register_sensors(self):
        """
        Add your sensors here.
        """

        # First, spin up the built-in sensors.
        super().register_sensors()

        # Add some sensors for the Hiveeyes project.
        log.info('Registering Hiveeyes sensors')

        # Scan and register configured list of environmental sensors.
        sensor_infos = self.settings.get('sensors.environment')

        # Backward compatibility.
        if sensor_infos is None:
            sensor_infos = self.settings.get('sensors.registry').values()

        for sensor_info in sensor_infos:
            sensor_id = sensor_info.get('id', sensor_info.get('key'))
            sensor_type = sensor_info.get('type')
            description = sensor_info.get('description')
            message = 'Setting up {} sensor with id "{}" described as "{}"'.format(sensor_type, sensor_id, description)
            log.info(message)
            try:

                if sensor_info.get('enabled') is False:
                    log.info('Sensor with id "{}" and type "{}" is disabled, '
                             'skipping registration'.format(sensor_id, sensor_type))
                    continue

                # Setup the HX711.
                if sensor_type == 'HX711':
                    self.add_hx711_sensor(sensor_info)

                # Setup the DS18X20.
                elif sensor_type == 'DS18B20':
                    self.add_ds18x20_sensor(sensor_info)

                # Setup the BME280.
                elif sensor_type == 'BME280':
                    self.add_bme280_sensor(sensor_info)

                else:
                    log.warning('Sensor with id={} has unknown type, skipping registration. '
                                'Sensor settings:\n{}'.format(sensor_id, sensor_info))

            except Exception as ex:
                log.exception('Setting up sensor with id={} and type={} failed'.format(sensor_id, sensor_type))

    def add_hx711_sensor(self, settings):
        """
        Setup and register the HX711 sensor component with your data logger.
        """

        if settings.get('enabled') is False:
            log.info("Skipping HX711 device on pins {}/{}".format(settings['pin_dout'], settings['pin_pdsck']))
            return

        from hiveeyes.sensor_hx711 import HX711Sensor
        hx711_sensor = HX711Sensor(settings=settings)
        hx711_sensor.set_address(settings.get('number', settings.get('address', 0)))
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

    def add_ds18x20_sensor(self, settings):
        """
        Setup and register the DS18X20  sensor component with your data logger.
        """
        from hiveeyes.sensor_ds18x20 import DS18X20Sensor

        bus = self.sensor_manager.get_bus_by_name(settings['bus'])
        sensor = DS18X20Sensor(settings=settings)
        sensor.acquire_bus(bus)

        # Start sensor.
        sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(sensor)

    def add_bme280_sensor(self, settings):
        """
        Setup and register the DS18X20  sensor component with your data logger.
        """

        bus = self.sensor_manager.get_bus_by_name(settings['bus'])

        if settings.get('enabled') is False:
            log.info("Skipping BME280 device {} on bus {}".format(hex(settings['address']), bus.name))
            return

        from hiveeyes.sensor_bme280 import BME280Sensor
        sensor = BME280Sensor(settings=settings)
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
