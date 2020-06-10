# -*- coding: utf-8 -*-
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys
import time
import socket
import machine
from terkin import logging
from terkin.util import format_exception, Eggtimer

log = logging.getLogger(__name__)


class NetworkManager:
    """ """

    def __init__(self, device, settings):
        self.device = device
        self.settings = settings

        self.device.watchdog.feed()

        self.wifi_manager = None
        self.lora_manager = None
        self.lte_manager = None
        self.gprs_manager = None

        self.mode_server = None
        self.http_api = None

    def stop(self):
        """ """
        self.stop_modeserver()

        # This helps the webserver to get rid of any listening sockets.
        # https://github.com/jczic/MicroWebSrv2/issues/8
        self.stop_httpserver()

        if self.wifi_manager:
            self.wifi_manager.stop()
            if self.device.status.maintenance is not True:
                self.wifi_manager.power_off()

        if self.lte_manager:
            self.lte_manager.stop()

    def start_wifi(self):
        """ """
        from terkin.network.wifi import WiFiManager
        self.wifi_manager = WiFiManager(manager=self, settings=self.settings)
        self.wifi_manager.start()

    def start_lora(self):
        """ """
        from terkin.network.lora import LoRaAdapter
        self.lora_manager = LoRaAdapter(network_manager=self, settings=self.settings)
        self.lora_manager.start()

    def start_lte(self):
        """ """
        from terkin.network.lte import SequansLTE
        self.lte_manager = SequansLTE(network_manager=self, settings=self.settings)
        self.lte_manager.start()

    def start_gprs(self):
        from terkin.network.gprs import GPRSManager
        self.gprs_manager = GPRSManager(manager=self, settings=self.settings)
        self.gprs_manager.start()

    def wait_for_ip_stack(self, timeout=5):
        """

        :param timeout:  (Default value = 5)

        """

        eggtimer = Eggtimer(duration=timeout)

        log.info('Waiting for the network stack to come up within %s seconds', timeout)
        while not eggtimer.expired():

            self.device.watchdog.feed()

            try:
                socket.getaddrinfo("localhost", 333)
                log.info('Network stack ready')
                return True

            except OSError as ex:
                #log.warning('Network stack not available: %s', format_exception(ex))
                pass

            # Report about progress.
            sys.stderr.write('.')
            #sys.stderr.flush()

            # Save power while waiting.
            machine.idle()
            time.sleep(0.25)

        # TODO: Make WiFi-agnostic.
        raise NetworkUnavailable('Could not connect to WiFi network')

    def wait_for_nic(self, timeout=5):
        """

        :param timeout:  (Default value = 5)

        """

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
        """ """

        # Start UDP server for pulling device into maintenance mode.
        if self.settings.get('services.api.modeserver.enabled', False):
            try:
                self.start_modeserver()
            except Exception as ex:
                log.exc(ex, 'Starting mode server failed')

        # Start HTTP server
        if self.settings.get('services.api.http.enabled', False):
            try:
                self.start_httpserver()
            except Exception as ex:
                log.exc(ex, 'Starting HTTP server failed')

    def start_modeserver(self):
        """Start UDP server for pulling device into maintenance mode."""

        # UDP server settings.
        #ip = self.wifi_manager.get_ip_address()
        ip = '0.0.0.0'
        port = self.settings.get('services.api.modeserver.port', 666)

        log.info('Starting mode server on {}:{}'.format(ip, port))
        from terkin.api.udp import UdpServer
        self.mode_server = UdpServer(ip, port)
        self.mode_server.start(self.handle_modeserver)

    def stop_modeserver(self):
        if self.mode_server:
            self.mode_server.stop()

    def start_httpserver(self):
        """Start HTTP server for managing the device."""
        from terkin.api.http import TerkinHttpApi
        storage = self.device.application_info.application.storage

        log.info('Setting up HTTP API')
        self.http_api = TerkinHttpApi(device=self.device, settings=self.settings, storage=storage)
        self.http_api.start()

    def stop_httpserver(self):
        if self.http_api:
            try:
                log.info('Shutting down HTTP server')
                self.http_api.stop()
            except Exception as ex:
                log.exc(ex, 'Shutting down HTTP server failed')

    def handle_modeserver(self, data, addr):
        """

        :param data: 
        :param addr: 

        """

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
    """ """
    pass
