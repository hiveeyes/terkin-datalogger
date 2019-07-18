# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import socket
import machine
from terkin import logging
from terkin.network.ip import UdpServer
from terkin.network.lora import LoRaManager
from terkin.network.wifi import WiFiManager
from terkin.util import format_exception

log = logging.getLogger(__name__)


class NetworkManager:

    def __init__(self, device, settings):
        self.device = device
        self.settings = settings

        self.device.watchdog.feed()

        self.wifi_manager = WiFiManager(manager=self, settings=self.settings)
        self.lora_manager = LoRaManager(manager=self, settings=self.settings)
        self.mode_server = None

    def stop(self):
        if self.device.status.maintenance is not True:
            self.wifi_manager.power_off()

    def start_wifi(self):
        self.wifi_manager.start()

    def start_lora(self):
        self.lora_manager.start()

    def wait_for_nic(self, retries=5):
        attempts = 0
        while attempts < retries:
            try:
                socket.getaddrinfo("localhost", 333)
                break
            except OSError as ex:
                log.warning('Network interface not available: %s', format_exception(ex))
            log.info('Waiting for network interface')
            # Save power while waiting.
            machine.idle()
            time.sleep(0.25)
            attempts += 1
        log.info('Network interface ready')

    def start_modeserver(self):
        """
        Start UDP server for pulling device into maintenance mode.
        """
        ip = self.wifi_manager.get_ip_address()
        port = 666
        log.info('Starting mode server on {}:{}'.format(ip, port))
        self.mode_server = UdpServer(ip, port)
        self.mode_server.start(self.handle_modeserver)

    def handle_modeserver(self, data, addr):

        message = data.decode()

        if message == 'maintenance.enable()':
            log.info('Enabling maintenance mode')
            self.device.status.maintenance = True
            self.device.watchdog.suspend()

        elif message == 'maintenance.disable()':
            log.info('Releasing maintenance mode')
            self.device.status.maintenance = False
            self.device.watchdog.resume()
