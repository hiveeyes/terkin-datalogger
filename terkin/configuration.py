# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import os_path
import json
import types
from copy import deepcopy
from dotty_dict import dotty
from shutil import copyfileobj
from terkin import logging
from terkin.backup import backup_file
from terkin.util import ensure_directory

log = logging.getLogger(__name__)


class TerkinConfiguration:
    """
    A flexible configuration manager.
    """

    CONFIG_PATH = '/flash'
    BACKUP_PATH = '/flash/backup'

    # Strip some settings when displaying configuration values
    # to prevent leaking sensible information into log files.
    # Todo: Should more things be optionally added here? E.g.
    # - Settings: ssid, endpoint, address
    # - Log: Device id, Networks (available|candidates), mac, ifconfig, Telemetry channel URI, MQTT broker
    protected_settings = [

        # WiFi
        'password',

        # LoRa
        'application_key', 'application_eui',
        
        # BEEP-BOB telemetry
        'key',
    ]

    def __init__(self):
        self.store = dotty()
        log.info('Starting TerkinConfiguration on path "{}"'.format(self.CONFIG_PATH))
        #os.stat(self.CONFIG_PATH)

        log.info('Ensuring existence of backup directory at "{}"'.format(self.BACKUP_PATH))
        ensure_directory(self.BACKUP_PATH)

    def get(self, key, default=None):
        return self.store.get(key, default=default)

    def set(self, key, value):
        self.store[key] = value
        return value

    def setdefault(self, key, default=None):
        return self.store.setdefault(key, default=default)

    def __delitem__(self, key):
        del self.store[key]

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

    def to_dict(self):
        return dict(self.store.to_dict())

    def save(self, filename, instream):
        """
        Save configuration file, with rotating backup.
        """
        import uos

        # Protect against directory traversals.
        filename = os_path.basename(filename)

        # Only allow specific filenames.
        if 'settings' not in filename:
            raise ValueError('Writing arbitrary files to the system is prohibited')

        # Absolute path to configuration file.
        filepath = os_path.join(self.CONFIG_PATH, filename)

        # Number of backup files to keep around.
        backup_count = self.get('main.backup.file_count', 7)

        # Backup configuration file.
        log.info('Backing up file {} to {}, keeping a history worth of {} files'.format(filepath, self.BACKUP_PATH, backup_count))
        backup_file(filepath, self.BACKUP_PATH, backup_count)

        # Overwrite configuration file.
        log.info('Saving configuration file {}'.format(filepath))
        with open(filepath, "w") as outstream:
            if isinstance(instream, str):
                outstream.write(instream)
            else:
                copyfileobj(instream, outstream)

        uos.sync()
