# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3


class HX711Sensor:
    """
    A generic HX711 sensor component wrapping possibly
    different hardware driver variants.

    After some boring parameter juggling, this sensors'
    ``read()`` method actually calls the hardware driver
    using ``self.loadcell.read_median()``.
    """

    def __init__(self, pin_dout=None, pin_pdsck=None, gain=None, scale=None, offset=None):

        print('INFO: Initializing HX711 sensor with '
              'DOUT={}, PD_SCK={}, GAIN={}, scale={}, offset={}'.format(pin_dout, pin_pdsck, gain, scale, offset))

        # Hardware parameters and configuration settings.
        self.pin_dout = pin_dout
        self.pin_pdsck = pin_pdsck
        self.gain = gain or 128
        self.scale = scale
        self.offset = offset

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

        print('INFO:  Selected HX711 hardware driver "{}"'.format(name))
        self.driver_class = HX711

    def start(self):

        # Initialize the HX711 hardware driver.
        try:
            self.loadcell = self.driver_class(self.pin_dout, self.pin_pdsck, self.gain)
        except Exception as ex:
            print('ERROR: HX711 hardware driver failed. {}'.format(ex))
            return

        # Configure the HX711 driver.
        if self.scale is not None:
            self.loadcell.set_scale(self.scale)
        if self.offset is not None:
            self.loadcell.set_offset(self.offset)

    def read(self):
        if self.loadcell is None:
            # TODO: Return Sensor.DISABLED
            return

        print('INFO: Acquire reading from HX711')
        value = self.loadcell.read_median()
        return {'weight': value}
