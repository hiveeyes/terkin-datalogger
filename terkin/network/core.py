# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import socket
import machine
from terkin import logging
from terkin.network.lora import LoRaManager
from terkin.network.wifi import WiFiManager
from terkin.util import format_exception

log = logging.getLogger(__name__)


class NetworkManager:

    def __init__(self, settings):
        self.settings = settings

        self.wifi_manager = WiFiManager(self.settings)
        self.lora_manager = LoRaManager(self.settings)

    def stop(self):
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
