from terkin import logging
from terkin.driver import hx711_sensor
from terkin.sensor import SensorManager, AbstractSensor

log = logging.getLogger(__name__)

def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create HX711 sensor object decorator for temperature compensation.

    Compensated load is calculated with the following formula:
        compensated_load = current_load + (temperature_offset - current_temp) * temp_compensation_factor

    :param sensor_manager:
    :param sensor_info:

    :return: decorator_object
    """

    log.info('Creating  hx711Sensor_object...')
    hx711Sensor_object = hx711_sensor.includeme(sensor_manager, sensor_info)
    log.info('Creating  HX711TempCompensationSensor...')
    decorator_object = HX711TempCompensationSensor(
        sensor_manager=sensor_manager, hx711Sensor_object=hx711Sensor_object, settings=sensor_info)
    
    decorator_object.family = hx711Sensor_object.family
    decorator_object.register_parameter('temperature_sensor_id', sensor_info['temperature_sensor_id'])
    decorator_object.register_parameter('temperature_offset', float(sensor_info['temperature_offset']))
    decorator_object.register_parameter('temp_compensation_factor', float(sensor_info['temp_compensation_factor']))

    log.info('HX711TempCompensationSensor created.')
    return decorator_object


class HX711TempCompensationSensor(AbstractSensor):
    """ Decorates HX7711Sensor class to add temperature compensation features
    """

    hx711Sensor_object = None
    sensor_manager = None

    def __init__(self, sensor_manager: SensorManager, hx711Sensor_object, settings=None):
        super().__init__(settings=settings)
        self.hx711Sensor_object = hx711Sensor_object
        self.sensor_manager = sensor_manager

    def start(self):
        """ """
        self.hx711Sensor_object.start()

    def read(self):
        """ """
        temperature = self.read_temperature()
        load_data = self.read_hx711_data()

        decorated_data = {}
        for key, value in load_data.items():
            if (key.startswith('weight')):
                decorated_data[key] = self.calculate_compensated_load(value, temperature)
            else:
                decorated_data[key] = value

        return decorated_data

    def power_on(self):
        """ """
        self.hx711Sensor_object.power_on()

    def power_off(self):
        """ """
        self.hx711Sensor_object.power_off()

    def calculate_compensated_load(self, weight, temperature):
        """ """
        tempOffset = self.parameter['temperature_offset']
        compensationFactor = self.parameter['temp_compensation_factor']

        compensated_weight = weight + (temperature - tempOffset) * compensationFactor
        log.info("weight compensation changed weight from '{}' to '{}'".format(weight, compensated_weight))
        return compensated_weight

    def read_temperature(self):
        """ """
        temp_sensor_id = self.parameter['temperature_sensor_id']
        log.info('reading temperature from {}'.format(temp_sensor_id))
        temp_sensor = self.sensor_manager.get_sensor_by_id(temp_sensor_id)
        
        temp_sensor_reading = temp_sensor.read()
        temp_sensor_data = temp_sensor_reading.data

        # Evaluate sensor outcome.
        if temp_sensor_data is None or temp_sensor_data is AbstractSensor.SENSOR_NOT_INITIALIZED:
            raise Exception("no temperature available")

        temperature = None
        for key, value in temp_sensor_data.items():
            if (key.startswith('temperature')):
                temperature = value
                break

        log.info('read temperature is {}'.format(temperature))
        if (temperature == None):
            raise Exception("no temperature available")

        return temperature

    def read_hx711_data(self):
        """ """
        log.info('reading sensor data from decorated hx711 sensor...')
        load_sensor_data = self.hx711Sensor_object.read()

        return load_sensor_data
