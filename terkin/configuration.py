# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import json
import types
from copy import deepcopy
from dotty_dict import dotty
from terkin import logging

log = logging.getLogger(__name__)


class TerkinConfiguration:
    """
    A flexible configuration manager.
    """

    # Strip some settings when displaying configuration values
    # to prevent leaking sensible information into log files.
    # Todo: Should more things be optionally added here? E.g.
    # - Settings: ssid, endpoint, address
    # - Log: Device id, Networks (available|candidates), mac, ifconfig, Telemetry channel URI, MQTT broker
    protected_settings = ['password', 'application_key', 'application_eui']

    def __init__(self):
        self.store = dotty()
        self.set_defaults()

    def get(self, key, default=None):
        return self.store.get(key, default=default)

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
            thing = deepcopy(value)
            self.purge_sensible_settings(thing)
            log.info('Section "{}": {}'.format(key, json.dumps(thing)))

    def purge_sensible_settings(self, thing):
        for key, value in thing.items():

            if isinstance(value, dict):
                self.purge_sensible_settings(value)

            elif isinstance(value, list):
                for item in value:
                    self.purge_sensible_settings(item)

            if key in self.protected_settings:
                value = '## redacted ##'
                thing[key] = value
