# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys
import time
import socket
import machine
from terkin import logging
from terkin.network.ip import UdpServer
from terkin.network.wifi import WiFiManager
from terkin.util import format_exception, Eggtimer

log = logging.getLogger(__name__)


class NetworkManager:

    def __init__(self, device, settings):
        self.device = device
        self.settings = settings

        self.device.watchdog.feed()

        self.wifi_manager = WiFiManager(manager=self, settings=self.settings)
        self.lora_manager = None
        self.mode_server = None

    def stop(self):
        if self.device.status.maintenance is not True:
            self.wifi_manager.power_off()

    def start_wifi(self):
        self.wifi_manager.start()

    def start_lora(self):
        from terkin.network.lora import LoRaManager
        self.lora_manager = LoRaManager(manager=self, settings=self.settings)
        self.lora_manager.start()

    def wait_for_ip_stack(self, timeout=5):

        eggtimer = Eggtimer(duration=timeout)

        log.info('Waiting for network stack')
        while not eggtimer.expired():

            self.device.watchdog.feed()

            try:
                socket.getaddrinfo("localhost", 333)
                log.info('Network stack ready')
                return True

            except OSError as ex:
                log.warning('Network stack not available', format_exception(ex))

            # Report about progress.
            sys.stderr.write('.')
            #sys.stderr.flush()

            # Save power while waiting.
            machine.idle()
            time.sleep(0.25)

        # TODO: Make WiFi-agnostic.
        raise NetworkUnavailable('Could not connect to WiFi network')

    def wait_for_nic(self, timeout=5):

        eggtimer = Eggtimer(duration=timeout)

        log.info('Waiting for network interface')
        while not eggtimer.expired():

            self.device.watchdog.feed()

            try:
                # TODO: Make WiFi-agnostic.
                if self.wifi_manager.is_connected():
                    log.info('Network interface ready')
                    return True

            except OSError as ex:
                log.warning('Network interface not available: %s', format_exception(ex))

            # Report about progress.
            sys.stderr.write('.')
            #sys.stderr.flush()

            # Save power while waiting.
            machine.idle()
            time.sleep(0.25)

        # TODO: Make WiFi-agnostic.
        raise NetworkUnavailable('Could not connect to WiFi network')

    def start_services(self):

        # Start UDP server for pulling device into maintenance mode.
        if self.settings.get('services.api.modeserver.enabled', False):
            try:
                self.start_modeserver()
            except:
                log.exception('Starting mode server failed')

        # Start HTTP server
        if self.settings.get('services.api.http.enabled', False):
            try:
                self.start_httpserver()
            except:
                log.exception('Starting HTTP server failed')

    def start_modeserver(self):
        """
        Start UDP server for pulling device into maintenance mode.
        """
        #ip = self.wifi_manager.get_ip_address()
        ip = '0.0.0.0'
        port = 666
        log.info('Starting mode server on {}:{}'.format(ip, port))
        self.mode_server = UdpServer(ip, port)
        self.mode_server.start(self.handle_modeserver)

    def start_httpserver(self):
        """
        Start HTTP server for managing the device.
        """
        from terkin.api.http import TerkinHttpApi
        storage = self.device.application_info.application.storage
        http_api = TerkinHttpApi(device=self.device, settings=self.settings, storage=storage)
        http_api.start()

    def handle_modeserver(self, data, addr):

        message = data.decode()

        if message == 'maintenance.enable()' and not self.device.status.maintenance:
            log.info('Enabling maintenance mode')
            self.device.status.maintenance = True
            self.device.watchdog.suspend()

        elif message == 'maintenance.disable()' and self.device.status.maintenance:
            log.info('Releasing maintenance mode')
            self.device.status.maintenance = False
            self.device.watchdog.resume()


class NetworkUnavailable(Exception):
    pass
