# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from unittest.mock import MagicMock

import pytest
from _pytest.monkeypatch import MonkeyPatch
from mocket.mocket import MocketSocket


class LoRaMock(MagicMock):

    def has_joined(self):
        return True


class LoRaNetworkFixture:

    LORA_RESPONSE_PORT = 0

    def __init__(self):

        self.monkeypatch = MonkeyPatch()

        import network
        self.monkeypatch.setattr('network.LoRa', LoRaMock(), raising=False)

        import socket
        self.monkeypatch.setattr('socket.AF_LORA', socket.AF_INET, raising=False)
        self.monkeypatch.setattr('socket.SOCK_RAW', socket.SOCK_STREAM, raising=False)
        self.monkeypatch.setattr('socket.socket', MocketSocket, raising=False)

    def register_conversation(self, response_port=None, response_data=None):
        from mocket import Mocket, MocketEntry

        response_port = response_port or self.LORA_RESPONSE_PORT
        response_data = response_data or []
        lora_entry = MocketEntry(location=(None, None), responses=response_data)
        lora_entry.request_cls = bytearray
        Mocket.reset()
        Mocket.register(lora_entry)

        def recvfrom(self, buffersize):
            if response_data:
                buffer = self.recv(buffersize)
                return buffer, response_port
            else:
                return None, response_port

        self.monkeypatch.setattr(MocketSocket, 'recvfrom', recvfrom, raising=False)

    def shutdown(self):
        self.monkeypatch.undo()


@pytest.fixture(scope='function')
def network_lora():
    fixture = LoRaNetworkFixture()
    yield fixture
    fixture.shutdown()
