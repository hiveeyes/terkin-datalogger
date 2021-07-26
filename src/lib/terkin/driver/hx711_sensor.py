# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import SensorManager, AbstractSensor

log = logging.getLogger(__name__)


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create HX711 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = HX711Sensor(settings=sensor_info)

    sensor_object.family = 'scale'
    sensor_object.set_address(sensor_info.get('number', sensor_info.get('address', 0)))
    sensor_object.register_pin('dout', sensor_info['pin_dout'])
    sensor_object.register_pin('pdsck', sensor_info['pin_pdsck'])
    sensor_object.register_parameter('scale', float(sensor_info['scale']))
    sensor_object.register_parameter('offset', float(sensor_info['offset']))
    sensor_object.register_parameter('gain', sensor_info.get('gain', 128))
    sensor_object.register_parameter('dualchannel', sensor_info.get('dualchannel', False))

    if "scaleB" in sensor_info:
        sensor_object.register_parameter('scaleB', float(sensor_info['scaleB']))
    if "offsetB" in sensor_info:
        sensor_object.register_parameter('offsetB', float(sensor_info['offsetB']))

    # Select driver module. Use "gerber" (vanilla) or "heisenberg" (extended).
    # hx711_sensor.select_driver('gerber')
    sensor_object.select_driver('heisenberg')

    return sensor_object


class HX711Sensor(AbstractSensor):
    """A generic HX711 sensor component wrapping possibly
    different hardware driver variants.
    
    After some boring parameter juggling, this sensors'
    ``read()`` method actually calls the hardware driver
    using ``self.loadcell.read_median()``.


    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # The driver class.
        self.driver_class = None

        # The driver instance.
        self.loadcell = None

    def select_driver(self, name='gerber'):
        """

        :param name:  (Default value = 'gerber')

        """

        # Use vanilla HX711 library by David Gerber.
        if name == 'gerber':
            from terkin.lib.hx711 import HX711

        # Use improved HX711 library by Ralf Lindlein.
        elif name == 'heisenberg':
            from terkin.lib.hx711_heisenberg import HX711Heisenberg as HX711

        # Error out for unknown hardware driver.
        else:
            raise ValueError('ERROR: Unknown HX711 hardware driver "{}"'.format(name))

        log.info('Selected HX711 hardware driver "{}"'.format(name))
        self.driver_class = HX711

    def start(self):
        """ """

        # Hardware parameters and configuration settings.
        pin_dout = self.pins['dout']
        pin_pdsck = self.pins['pdsck']
        gain = self.parameter.get('gain', 128)
        scale = self.parameter['scale']
        offset = self.parameter['offset']

        # Initialize the HX711 hardware driver.
        log.info('Initializing HX711 sensor with '
                 'pin_dout={}, pin_pdsck={}, gain={}, scale={}, offset={}'.format(pin_dout, pin_pdsck, gain, scale, offset))
        if self.parameter['dualchannel']:
            scaleB = self.parameter['scaleB']
            offsetB = self.parameter['offsetB']
            log.info('Initializing HX711 sensor channel B with gain=32 '
                    'scale={}, offset={}'.format(scaleB, offsetB))

        try:
            self.loadcell = self.driver_class(pin_dout, pin_pdsck, gain)

            # Configure the HX711 driver.
            if self.parameter['scale'] is not None:
                self.loadcell.set_scale(self.parameter['scale'])
            if self.parameter['offset'] is not None:
                self.loadcell.set_offset(self.parameter['offset'])

            return True

        except Exception as ex:
            log.exc(ex, 'HX711 hardware driver failed. Reason: {}'.format(ex))

    def read(self):
        """ """
        if self.loadcell is None:
            return self.SENSOR_NOT_INITIALIZED

        address = self.address

        #log.info('Acquire reading from HX711')
        readingA = self.loadcell.get_reading()

        # with dualchannel 3 data sets are generated instead of one
        # 1 - cumulated weight, no parameter, 2 - channel A reading with parameters, 3 - same for channel B
        if self.parameter['dualchannel']:   # read channel B
            self.loadcell.set_gain(32)      # switch to channel B
            self.loadcell.set_scale(self.parameter['scaleB'])
            self.loadcell.set_offset(self.parameter['offsetB'])
            readingB = self.loadcell.get_reading()
            self.loadcell.set_gain(self.parameter.get('gain', 128))      # switch everything back
            self.loadcell.set_scale(self.parameter['scale'])
            self.loadcell.set_offset(self.parameter['offset'])

            # Propagate main kg value.
            key = 'weight.{}'.format(address)
            totalweight = readingA.kg + readingB.kg
            effective_data = {
                key: totalweight
            }
            # Propagate _all_ values from HX711 channel A (raw, scale, offset, whatever).
            data = readingA.get_data()
            for key, value in data.items():
                effective_key = 'scaleA.{}.{}'.format(address, key)
                effective_data[effective_key] = value
            # Propagate _all_ values from HX711 channel B (raw, scale, offset, whatever).
            data = readingB.get_data()
            for key, value in data.items():
                effective_key = 'scaleB.{}.{}'.format(address, key)
                effective_data[effective_key] = value

        else:

            # Propagate main kg value.
            key = 'weight.{}'.format(address)
            effective_data = {
                key: readingA.kg
            }
            # Propagate _all_ values from HX711 (raw, scale, offset, whatever).
            data = readingA.get_data()
            for key, value in data.items():
                effective_key = 'scale.{}.{}'.format(address, key)
                effective_data[effective_key] = value

        return effective_data

    def power_on(self):
        """ """
        log.info('Powering up HX711')
        if self.loadcell:
            self.loadcell.power_up()

    def power_off(self):
        """ """
        log.info('Powering down HX711')
        if self.loadcell:
            self.loadcell.power_down()
