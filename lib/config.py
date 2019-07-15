import json
import os
import machine

class Config:
    def __init__(self):
        self.path_user_settings = '/flash/user_settings.json'
        self.path_default_settings = '/flash/default_settings.json'
        self.read_settings()

    def _read_json_file(self, path):
        content = {}
        try:
            with open(path, 'r') as file_:
                content = json.load(file_)
        except OSError as e:
            print("File not found: {}".format(e))
        finally:
            return content

    def read_settings(self):
        self.default_settings = self._read_json_file(self.path_default_settings)
        self.user_settings = self._read_json_file(self.path_user_settings)

    def get_subsection(self, section, subsection):
        values = self.default_settings[section][subsection]
        try:
            user_values = self.user_settings[section][subsection]
        except KeyError:
            user_values = {}

        for key, val in user_values.items():
            values[key] = val

        return values

    def set_subsection(self, section, subsection, data):
        for key, val in data.items():
            self.set_value(section, subsection, key, val)
        self.write()

    def get_value(self, section, subsection, key):
        value = None
        try:
            value = self.user_settings[section][subsection][key]
        except KeyError:
            value = self.default_settings[section][subsection][key]
        finally:
            return value

    def set_value(self, section, subsection, key, value):
        if self.default_settings[section][subsection][key] != value:
            if section not in self.user_settings.keys():
                self.user_settings[section] = {}
            if subsection not in self.user_settings[section].keys():
                self.user_settings[section][subsection] = {}
            self.user_settings[section][subsection][key] = value


    def write(self, i=0):
        with open(self.path_user_settings, 'w') as file_:
            file_.write(json.dumps(self.user_settings))
        os.sync()
        if os.stat(self.path_user_settings)[6] == 0 and i < 3:
            print("Error: Saving settings failed. Retry...")
            self.write(i=i+1)
        elif i >= 3:
            print("Error: Unable to save settings.")
