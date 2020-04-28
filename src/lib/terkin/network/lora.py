# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import socket
from terkin import logging
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()


class LoRaAdapter:

    def __init__(self, network_manager, settings):
        self.network_manager = network_manager
        self.settings = settings

        # LoRa settings.
        self.otaa_settings = self.settings.get('networking.lora.otaa')
        #self.generated_device_eui = binascii.hexlify(LoRa().mac())

        # Pycom MicroPython
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            self.driver = LoRaDriverPycom(self.network_manager, self.settings)

        # RaspberryPi (Dragino)
        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
            self.driver = LoRaDriverDragino(self.network_manager, self.settings)

    def start(self):
        log.info('[LoRa] Starting LoRa Adapter')
        return self.driver.start()
    
    def ensure_connectivity(self):
        return self.driver.ensure_connectivity()

    def send(self, payload):
        return self.driver.send(payload)

    def receive(self):
        return self.driver.receive()


class LoRaDriverPycom:
    """ """

    def __init__(self, network_manager, settings):
        self.network_manager = network_manager
        self.settings = settings

        # LoRa settings.
        self.otaa_settings = self.settings.get('networking.lora.otaa')
        #self.generated_device_eui = binascii.hexlify(LoRa().mac())

    def start(self):
        """ """

        from network import LoRa

        if self.otaa_settings['region']   == 'AS923':
            lora_region = LoRa.AS923
        elif self.otaa_settings['region'] == 'AU915':
            lora_region = LoRa.AU915
        elif self.otaa_settings['region'] == 'EU868':
            lora_region = LoRa.EU868
        elif self.otaa_settings['region'] == 'US915':
            lora_region = LoRa.US915

        lora_adr = self.otaa_settings['adr'] or False

        self.lora_socket = None

        self.lora = LoRa(mode=LoRa.LORAWAN, region=lora_region, adr=lora_adr)

        # Restore LoRa state from NVRAM after waking up from DEEPSLEEP.
        # Otherwise, reset LoRa NVRAM and rejoin.
        import machine
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            self.lora.nvram_restore()
            log.info('[LoRa] LoRaWAN state restored from NVRAM after deep sleep')
        else:
            self.lora.nvram_erase()
            log.info('[LoRa] LoRaWAN state erased from NVRAM. Rejoin forced')

        # Create LoRaWAN OTAA connection to TTN.
        import binascii
        app_eui = binascii.unhexlify(self.otaa_settings['application_eui'])
        app_key = binascii.unhexlify(self.otaa_settings['application_key'])

        if not self.lora.has_joined():
            log.info('[LoRa] Joining the network')
            if self.otaa_settings.get('device_eui') is None:
                self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
            else:
                dev_eui = binascii.unhexlify(self.otaa_settings['device_eui'])
                self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=0)

    def ensure_connectivity(self):
        self.wait_for_lora_join(42)

        if self.lora_joined:
            if self.lora_socket is None:
                try:
                    self.create_socket()
                except:
                    log.exception("[LoRa] Could not create LoRa socket")
        else:
            log.error("[LoRa] Could not join network")

    def wait_for_lora_join(self, attempts):
        """

        :param attempts: 

        """
        self.lora_joined = None
        for i in range(0, attempts):
            while not self.lora.has_joined():
                log.info('[LoRa] Not joined yet...')
                time.sleep(2.5)

        self.lora_joined = self.lora.has_joined()

        if self.lora_joined:
            log.info('[LoRa] Joined successfully')
        else:
            log.info('[LoRa] Did not join in %s attempts', attempts)

        return self.lora_joined

    def create_socket(self):
        """ """

        # create a lora socket
        self.socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        self.socket.settimeout(6.0)

        self.lora_socket = True
        log.info('[LoRa] Socket created')

        return self.lora_socket

    def send(self, payload):
        """

        :param payload: 

        """
        self.socket.setblocking(True)

        success = self.socket.send(payload)

        self.socket.setblocking(False)

        self.lora.nvram_save()

        return success

    def receive(self):
        """ """

        try:
            rx, port = self.socket.recvfrom(256)
        except socket.timeout:
            log.info('[LoRa] No packet received within receive window')

        if rx:
            log.info('[LoRa] Received: {} on port: {}'.format(rx, port))

        return rx, port


class LoRaDriverDragino:
    """ """

    def __init__(self, network_manager, settings):
        self.network_manager = network_manager
        self.settings = settings

        self.otaa_settings = self.settings.get('networking.lora.otaa')

        self.dragino = None
        self.setup()

    def setup(self):
        log.info('[LoRa] Setting up LoRa')

        # Monkeypatch SX127x library
        from dragino.SX127x.board_config import BOARD
        BOARD.DIO3 = None

        from dragino.dragino import Dragino, LoRaWANAuthentication, LoRaWANConfig
        lora_auth = LoRaWANAuthentication(auth_mode='OTAA',
                                          deveui=self.otaa_settings['device_eui'],
                                          appeui=self.otaa_settings['application_eui'],
                                          appkey=self.otaa_settings['application_key'])
        lora_config = LoRaWANConfig(auth=lora_auth)
        self.dragino = Dragino(config=lora_config)

    def start(self):
        log.info('[LoRa] Starting join')
        self.dragino.join()

    def ensure_connectivity(self):
        while not self.dragino.registered():
            log.info('[LoRa] Waiting for connectivity')
            time.sleep(1)

    def send(self, payload):
        return self.dragino.send_bytes(list(payload))

    def receive(self):
        return None, None
