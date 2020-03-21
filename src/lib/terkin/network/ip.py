# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging

log = logging.getLogger(__name__)


class UdpServer:
    """ """

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.callback = None

        self.server_socket = None
        self.is_running = False

    def start(self, callback=None):
        """

        :param callback:  (Default value = None)

        """
        self.callback = callback
        import _thread
        self.is_running = True
        _thread.start_new_thread(self.start_real, ())

    def stop(self):
        self.is_running = False
        log.info("Shutting down UdpServer")
        self.server_socket.close()

    def start_real(self):
        """ """
        import socket

        log.info("Starting UdpServer on {}:{}".format(self.ip, self.port))
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.ip, self.port))

        except Exception as ex:
            log.exc(ex, "Failed starting UdpServer on {}:{}".format(self.ip, self.port))
            return

        try:
            while self.is_running:
                data, addr = self.server_socket.recvfrom(1024)
                self.receive_handler(data, addr)
                self.server_socket.sendto(data, addr)

        except KeyboardInterrupt:
            log.info("Received KeyboardInterrupt within UdpServer")
            self.stop()
            raise

    def receive_handler(self, data, addr):
        """

        :param data: 
        :param addr: 

        """
        log.info('UdpServer received {} from {}'.format(data, addr))
        if callable(self.callback):
            self.callback(data, addr)
