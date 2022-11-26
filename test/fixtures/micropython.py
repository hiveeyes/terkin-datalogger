# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import pytest


@pytest.fixture(scope='function', autouse=True)
def micropython_stdlib(monkeypatch):
    # Adjust modules.
    # Use the one provided through "dist-packages"
    # and not the one from CPython stdlib.
    import sys
    monkeypatch.delitem(sys.modules, 'urllib.parse')
    monkeypatch.delitem(sys.modules, 'urllib')
    monkeypatch.delitem(sys.modules, 'base64')
    monkeypatch.delitem(sys.modules, 'shutil')
