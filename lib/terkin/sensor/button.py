# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from machine import Timer
from terkin import logging
from terkin.sensor.touch import TouchPad

log = logging.getLogger(__name__)


class Button:
    """ """
    def __init__(self, name, location, adapter):
        self.name = name
        self.location = location
        self.adapter = adapter

        self.enabled = True

    @property
    def pin(self):
        """ """
        return self.adapter.pin

    def __str__(self):
        return 'Button {} (pin {}) at {}'.format(self.name, self.pin, self.location)


class ButtonManager:
    """ """

    check_interval_ms = 10

    def __init__(self):

        log.info('Initializing button manager')

        # Initialize the buttons.
        self.buttons = []

        # Enable the alarm to check the status.
        self.alarm = Timer.Alarm(self.check, ms=self.check_interval_ms, periodic=True)

    def setup_touchpad(self, pin, name, location):
        """

        :param pin: 
        :param name: 
        :param location: 

        """
        try:
            button = Button(
                name=name,
                location=location,
                adapter=TouchPad(pin, name, sensitivity=1000, duration=500),
            )
            log.info('Setting up %s', button)
            self.buttons.append(button)
        except Exception as ex:
            log.exc(ex, 'Setting up button on pin {} failed'.format(pin))

    def check(self, alarm):
        """

        :param alarm: 

        """
        for button in self.buttons:
            if not button.enabled:
                continue
            try:
                if button.adapter.is_pressed() and not button.adapter.just_pressed():
                    log.info('{} pressed'.format(button))
                    button.adapter.set_press()
            except Exception as ex:
                button.enabled = False
                log.exc(ex, 'Checking {} failed'.format(button))
