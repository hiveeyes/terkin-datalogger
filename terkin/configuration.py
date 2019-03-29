# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import json
import types
from dotty_dict import dotty
from terkin import logging

log = logging.getLogger(__name__)


class TerkinConfiguration:
    """
    A flexible configuration manager.
    """

    def __init__(self):
        self.store = dotty()
        self.set_defaults()

    def get(self, key):
        return self.store.get(key)

    def set_defaults(self):
        self.store.setdefault('networking.wifi.stations', [])

    def add(self, data):
        try:
            self.add_real(data)
        except Exception as ex:
            log.exception('Reading configuration settings failed')

    def add_real(self, data):
        if isinstance(data, types.ModuleType):
            blacklist = ['__name__', '__file__', '__class__']
            for key in dir(data):
                if key in blacklist: continue
                value = getattr(data, key)
                self.store[key] = value

    def dump(self):
        log.info('Configuration settings:')
        for key, value in self.store.items():
            log.info('Section "{}": {}'.format(key, json.dumps(value)))
