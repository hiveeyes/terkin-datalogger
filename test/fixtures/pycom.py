# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import pytest
from _pytest.monkeypatch import MonkeyPatch


class NVRAMFixture:

    def __init__(self):
        self.storage = {}
        self.monkeypatch = MonkeyPatch()
        self.monkeypatch.setattr('pycom.nvs_set', self.nvs_set, raising=False)
        self.monkeypatch.setattr('pycom.nvs_get', self.nvs_get, raising=False)

    def nvs_set(self, key, value):
        self.storage[key] = value

    def nvs_get(self, key):
        if key not in self.storage:
            raise KeyError('"{}" not in NVRAM'.format(key))
        return self.storage.get(key)

    def shutdown(self):
        self.monkeypatch.undo()


@pytest.fixture(scope='function', autouse=True)
def pycom_nvram():
    fixture = NVRAMFixture()
    yield fixture
    fixture.shutdown()
