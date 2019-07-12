# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging

log = logging.getLogger(__name__)


class UdpServer:

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.callback = None

    def start(self, callback=None):
        self.callback = callback
        import _thread
        _thread.start_new_thread(self.start_real, ())

    def start_real(self):
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port))
        print('waiting....')
        while True:
            data, addr = s.recvfrom(1024)
            self.receive_handler(data, addr)
            s.sendto(data, addr)

    def receive_handler(self, data, addr):
        log.info('UdpServer received {} from {}'.format(data, addr))
        if callable(self.callback):
            self.callback(data, addr)
