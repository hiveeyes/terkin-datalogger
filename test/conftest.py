# Monkeypatch the whole machinery to be executable on CPython.
import pytest
from pyfakefs.fake_filesystem_unittest import Patcher

from test.util.micropython import monkeypatch
monkeypatch()

from test.util.terkin import monkeypatch_terkin
monkeypatch_terkin()

from test.util.adafruit import monkeypatch
monkeypatch()

from test.fixtures import *


@pytest.fixture
def fs_no_root():
    with Patcher(allow_root_user=False) as patcher:
        yield patcher.fs
