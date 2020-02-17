# -*- coding: utf-8 -*-
#
# Ratrack MicroPython Datalogger
# https://github.com/hiveeyes/terkin-datalogger
#
# (c) 2019 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
from terkin import logging
from terkin.datalogger import TerkinDatalogger
from terkin.telemetry import to_cayenne_lpp
from hiveeyes.sensor_bme280 import BME280Sensor
from hiveeyes.sensor_pytrack import PytrackSensor
from ratrack import convert
from ratrack.sensor_adc import MoistureSensor, WaterlevelSensor
import time

log = logging.getLogger(__name__)


class RatrackDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This time for MicroPython.
    """

    # Naming things.
    name = 'Ratrack MicroPython Datalogger'

    def __init__(self, settings):
        self.data = None
        super().__init__(settings)

    def register_sensors(self):
        """
        Add your sensors here.
        """

        # First, spin up the built-in sensors.
        super().register_sensors()

        # Add some project-specific sensors.
        log.info('Registering Ratrack sensors')

        # Setup the BME280.
        try:
            self.add_bme280_1_sensor()
        except Exception as ex:
            print('INFO:  Skipping bme280 sensor. {}'.format(ex))

        # Setup the BME280.
        try:
            self.add_bme280_sensor()
        except Exception as ex:
            log.exception('Skipping bme280 sensor')

        # Setup the Moisture Sensor.
        try:
            self.add_moisture_sensor()
        except Exception as ex:
            print('INFO:  Skipping Moisture sensor. {}'.format(ex))

        # Setup the Waterlevel Sensor.
        try:
            self.add_waterlevel_sensor()
        except Exception as ex:
            print('INFO:  Skipping Waterlevel sensor. {}'.format(ex))

        # Setup the Pytrack.
        try:
            self.add_pytrack_sensor()
        except Exception as ex:
            log.exception('Skipping Pytrack sensor')

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

    def add_bme280_1_sensor(self):
        """
        Setup and register the DS18X20  sensor component with your data logger.
        """

        settings = self.settings.get('sensors.registry.bme280_1')
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

    def add_moisture_sensor(self):
        """
        Setup and register the Moisture sensor component with your data logger.
        """

        # Initialize Moisture sensor component.
        settings = self.settings.get('sensors.registry.moisture')

        sensor = MoistureSensor()
        sensor.register_pin('adc_in', settings['pin_adc_in'])
        sensor.register_parameter('scaling', settings['scaling'])

        # Start sensor.
        sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(sensor)

    def add_waterlevel_sensor(self):
        """
        Setup and register the Waterlevel sensor component with your data logger.
        """

        # Initialize waterlevel sensor component.
        settings = self.settings.get('sensors.registry.waterlevel')

        sensor = WaterlevelSensor()
        sensor.register_pin('adc_in', settings['pin_adc_in'])

        # Start sensor.
        sensor.start()

        # Register with framework.
        self.sensor_manager.register_sensor(sensor)

    def read_sensors(self):
        self.data = super().read_sensors()
        return self.data

    def loop(self):
        """
        Loop function. Do what I mean.
        """

        # Finally, schedule other system tasks.
        super().loop()
        print('SelfData:', self.data)

        # It's your turn.
        if self.settings.get('networking.lora.antenna_attached'):
            #if self.serialize_and_send():
            if self.to_cayenne_lpp_and_send():
                log.info('[LoRa] Success')


    def to_cayenne_lpp_and_send(self):
        if self.data is None:
            return

            # Create Byte Payload for LoRa.
        try:
            payload = self.to_cayenne_lpp_ratrack()
        except:
            log.exception('[LoRa] Serialization failed')
            return False

            # Send to the wire.
        try:
            lora_received = self.device.networking.lora_send(payload)
            print(lora_received)
        except:
            log.exception('[LoRa] Transmission failed')
            return False

        return True

    def serialize_and_send(self):
        if self.data is None:
            return

        if 'longitude' not in self.data:
            self.data['longitude'] = 0.0
            self.data['latitude'] = 0.0
            self.data['speed'] = 0.0
            self.data['cog'] = 0.0

        # Create Byte Payload for LoRa.
        try:
            payload = convert.create_payload(self.data)
        except:
            log.exception('[LoRa] Serialization failed')
            return False

        # Send to the wire.
        try:
            lora_received = self.device.networking.lora_send(payload)
            print(lora_received)
        except:
            log.exception('[LoRa] Transmission failed')
            return False

        return True

    def to_cayenne_lpp_ratrack(self):
        """
        Serialize plain data dictionary to binary CayenneLPP format.
        """
        data = self.data

        from cayennelpp import LppFrame
        # create empty frame
        frame = LppFrame()


        channel = 1
        # add some sensor data
        if 'temperature' in data:
            try:
                frame.add_temperature(channel, data.get('temperature'))
            except:
                log.exception('[Cayenne] Serialization failed')

        #if 'humidity' in data:
        #    try:
        #        frame.add_humitidy(channel, data.get('add_humidity'))
        #    except:
        #        log.exception('[Cayenne] Serialization failed')

        if 'pressure' in data:
            try:
                frame.add_barometer(channel, data.get('pressure'))
            except:
                log.exception('[Cayenne] Serialization failed')

        if 'speed' in data and 'roll' in data and 'pitch' in data:
            try:
                frame.add_gyrometer(channel, data.get('speed'), data.get('roll'), data.get('pitch'))
            except:
                log.exception('[Cayenne] Serialization failed')

        if 'battery_voltage' in data:
            try:
                frame.add_analog_input(channel, data.get('battery_voltage'))
            except:
                log.exception('[Cayenne] Serialization failed')

        if 'latitude' in data and 'longitude' in data and 'altitude' in data:
            try:
                log.info('GPS to Cayenne')
                frame.add_gps(channel, data.get('latitude'), data.get('longitude'), data.get('altitude'))
            except:
                log.exception('[Cayenne] Serialization failed')

        #channel = 2
        #if 'cog' in data:
        #    try:
        #        frame.add_analog_input(channel, data.get('cog'))
        #    except:
        #        log.exception('[Cayenne] Serialization failed')

        channel = 3
        if 'memfree' in data:
            try:
                frame.add_analog_input(channel, data.get('memfree'))
            except:
                log.exception('[Cayenne] Serialization failed')

        channel = 4
        if 'waterlevel_volt' in data:
            try:
                frame.add_analog_input(channel, data.get('waterlevel_volt'))
            except:
                log.exception('[Cayenne] Serialization failed')

        channel = 5
        if 'moisture_volt' in data:
            try:
                frame.add_analog_input(channel, data.get('moisture_volt'))
            except:
                log.exception('[Cayenne] Serialization failed')

        return frame.bytes()
