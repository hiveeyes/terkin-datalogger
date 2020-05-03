# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import json
import types
import os_path
from copy import deepcopy
from dotty_dict import dotty
from shutil import copyfileobj
from terkin import logging
from terkin.backup import backup_file
from terkin.util import ensure_directory, get_platform_info, deepupdate

log = logging.getLogger(__name__)


class TerkinConfiguration:
    """A flexible configuration manager."""

    USER_SETTINGS_FILE = 'settings-user.json'

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
        self.overlay = dotty()

        self.record = True

        self.compute_paths()

        log.info('Starting TerkinConfiguration on path "{}"'.format(self.CONFIG_PATH))
        #os.stat(self.CONFIG_PATH)

        if self.get('main.backup.enabled', False):
            try:
                log.info('Ensuring existence of backup directory at "{}"'.format(self.BACKUP_PATH))
                ensure_directory(self.BACKUP_PATH)
            except Exception as ex:
                log.exc(ex, 'Ensuring existence of backup directory at "{}" failed'.format(self.BACKUP_PATH))

    def __getitem__(self, key, default=None):
        return self.get(key, default=default)

    def __setitem__(self, key, value):
        return self.set(key, value)

    def __delitem__(self, key):
        del self.store[key]

    def compute_paths(self):
        platform_info = get_platform_info()
        if platform_info.vendor == platform_info.MICROPYTHON.Pycom:
            self.CONFIG_PATH = '/flash'
            self.BACKUP_PATH = '/flash/backup'
        elif platform_info.vendor == platform_info.MICROPYTHON.Vanilla:
            self.CONFIG_PATH = '/'
            self.BACKUP_PATH = '/backup'
        else:
            self.CONFIG_PATH = os.path.abspath('.')
            self.BACKUP_PATH = os.path.join(self.CONFIG_PATH, 'backup')

    def get(self, key, default=None):
        """

        :param key: 
        :param default:  (Default value = None)

        """
        return self.store.get(key, default=default)

    def set(self, key, value):
        """

        :param key: 
        :param value: 

        """
        self.store[key] = value
        if self.record:
            self.overlay[key] = value
            self.save(self.USER_SETTINGS_FILE, json.dumps(self.overlay.to_dict()))
        return value

    def setdefault(self, key, default=None):
        """

        :param key: 
        :param default:  (Default value = None)

        """
        # TODO: Add recording functionality.
        return self.store.setdefault(key, default=default)

    def add(self, data):
        """

        :param data: 

        """
        self.record = False
        try:
            self.add_real(data)
        except Exception as ex:
            log.exc(ex, 'Reading configuration settings failed')
        self.record = True

    def add_real(self, data):
        """

        :param data: 

        """
        if isinstance(data, types.ModuleType):
            blacklist = ['__name__', '__file__', '__class__']
            for key in dir(data):
                if key in blacklist: continue
                value = getattr(data, key)
                self.store[key] = value

    def dump(self):
        """ """
        log.info('Configuration settings:')
        for key, value in self.store.items():
            if key.startswith('__'):
                continue
            thing = deepcopy(value)
            self.purge_sensible_settings(thing)
            log.info('Section "{}": {}'.format(key, json.dumps(thing)))

    def purge_sensible_settings(self, thing):
        """
        This function purges all sensible pieces from the data structure
        holding the configuration settings in order to protect information
        leakage os sensitive information to STDOUT.

        :param thing: 
        """
        if isinstance(thing, dict):
            for key, value in thing.items():

                if key in self.protected_settings:
                    value = '## redacted ##'
                    thing[key] = value

                self.purge_sensible_settings(value)

        elif isinstance(thing, list):
            for item in thing:
                self.purge_sensible_settings(item)

    def to_dict(self):
        """ """
        return dict(self.store.to_dict())

    def add_user_file(self):
        """ """
        data = self.load(self.USER_SETTINGS_FILE)
        log.info('User settings: %s', data)
        if data is not None:
            self.overlay.update(data)
            deepupdate(self.store, self.overlay)

    def load(self, filename):
        """Load configuration file.

        :param filename: 

        """
        # Protect against directory traversals.
        filename = os_path.basename(filename)

        # Absolute path to configuration file.
        filepath = os_path.join(self.CONFIG_PATH, filename)

        # FIXME: Use ``os_path.exists``.
        try:
            os.stat(filepath)
        except OSError:
            return

        log.info('Reading configuration file {}'.format(filepath))
        try:
            with open(filepath, "r") as instream:
                payload = instream.read()
                data = json.loads(payload)
                return data

        except Exception as ex:
            log.exc(ex, 'Reading configuration from "{}" failed'.format(filepath))

    def save(self, filename, instream):
        """Save configuration file, with rotating backup.

        :param filename: 
        :param instream: 

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
            outstream.flush()

        uos.sync()
