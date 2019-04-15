# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import AbstractSensor

log = logging.getLogger(__name__)


class HX711Sensor(AbstractSensor):
    """
    A generic HX711 sensor component wrapping possibly
    different hardware driver variants.

    After some boring parameter juggling, this sensors'
    ``read()`` method actually calls the hardware driver
    using ``self.loadcell.read_median()``.
    """

    def __init__(self):

        super().__init__()

        # The driver class.
        self.driver_class = None

        # The driver instance.
        self.loadcell = None

    def select_driver(self, name='gerber'):

        # Use vanilla HX711 library by David Gerber.
        if name == 'gerber':
            from hx711 import HX711

        # Use improved HX711 library by Ralf Lindlein.
        elif name == 'heisenberg':
            from hx711_heisenberg import HX711Heisenberg as HX711

        # Error out for unknown hardware driver.
        else:
            raise ValueError('ERROR: Unknown HX711 hardware driver "{}"'.format(name))

        log.info('Selected HX711 hardware driver "{}"'.format(name))
        self.driver_class = HX711

    def start(self):

        # Hardware parameters and configuration settings.
        pin_dout = self.pins['dout']
        pin_pdsck = self.pins['pdsck']
        gain = self.parameter.get('gain', 128)
        scale = self.parameter['scale']
        offset = self.parameter['offset']

        # Initialize the HX711 hardware driver.
        log.info('Initializing HX711 sensor with '
                 'pin_dout={}, pin_pdsck={}, gain={}, scale={}, offset={}'.format(pin_dout, pin_pdsck, gain, scale, offset))

        try:
            self.loadcell = self.driver_class(pin_dout, pin_pdsck, gain)

            # Configure the HX711 driver.
            if self.parameter['scale'] is not None:
                self.loadcell.set_scale(self.parameter['scale'])
            if self.parameter['offset'] is not None:
                self.loadcell.set_offset(self.parameter['offset'])

            return True

        except Exception as ex:
            log.exception('HX711 hardware driver failed')

    def read(self):
        if self.loadcell is None:
            return self.SENSOR_NOT_INITIALIZED

        #log.info('Acquire reading from HX711')
        value = self.loadcell.read_median()
        return {'weight': value}
