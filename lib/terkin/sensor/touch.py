# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from terkin import logging

"""
==================
ESP32 Touch Sensor
==================

A touch-sensor system is built on a substrate which carries electrodes and 
relevant connections under a protective flat surface. When a user touches 
the surface, the capacitance variation is triggered and a binary signal is 
generated to indicate whether the touch is valid.

ESP32 can provide up to 10 capacitive touch pads / GPIOs. The sensing pads 
can be arranged in different combinations (e.g. matrix, slider), so that a 
larger area or more points can be detected. The touch pad sensing process 
is under the control of a hardware-implemented finite-state machine (FSM) 
which is initiated by software or a dedicated hardware timer.

- https://docs.pycom.io/tutorials/all/touch.html
- https://github.com/espressif/esp-iot-solution/blob/master/documents/touch_pad_solution/touch_sensor_design_en.md
- https://docs.espressif.com/projects/esp-idf/en/latest/api-reference/peripherals/touch_pad.html
- https://github.com/espressif/esp-idf/tree/58df1d93b/examples/peripherals/touch_pad_read
- https://www.instructables.com/id/ESP32-With-Capacitive-Touch-Button/
- https://microcontrollerslab.com/esp32-touch-sensor-button-example/

FiPy Pinout
-----------
- https://pycom.io/wp-content/uploads/2018/08/fipyPinoutNewCompN.pdf
"""

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)


class TouchPad:
    """From https://docs.pycom.io/tutorials/all/touch.html"""

    def __init__(self, pin, name, sensitivity, duration):
        self.name = name
        self.pin = pin
        self.sensitivity = sensitivity
        self.duration = duration

        self.touch = None
        self.last_press = 0
        self.pressed = False

        self.setup()

    def setup(self):
        """ """
        from machine import Touch
        self.touch = Touch(self.pin)
        self.touch.init_value(self.sensitivity)

    def read(self):
        """ """
        value = self.touch.read()
        log.debug('value: %s %s', self.name, value)
        return value

    def is_pressed(self):
        """ """
        # Todo: Review these magic values ``* 2 / 3``.
        threshold = self.touch.init_value() * 2 / 3
        if self.read() < threshold:
            self.pressed = True
        else:
            self.pressed = False
        return self.pressed

    def just_pressed(self):
        """ """
        now = time.ticks_ms()
        if now - self.last_press < self.duration:
            return True
        else:
            return False

    def set_press(self):
        """ """
        self.last_press = time.ticks_ms()
