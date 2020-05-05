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
    """
    LoRa driver for Pycom MicroPython
    """

    def __init__(self, network_manager, settings):
        self.network_manager = network_manager
        self.settings = settings

    def start(self):
        """ Start driver """

        from network import LoRa

        if self.settings.get('networking.lora.region')   == 'AS923':
            lora_region = LoRa.AS923
        elif self.settings.get('networking.lora.region') == 'AU915':
            lora_region = LoRa.AU915
        elif self.settings.get('networking.lora.region') == 'EU868':
            lora_region = LoRa.EU868
        elif self.settings.get('networking.lora.region') == 'US915':
            lora_region = LoRa.US915

        lora_adr = self.settings.get('networking.lora.adr') or False

        self.lora_socket = None

        self.lora = LoRa(mode=LoRa.LORAWAN, region=lora_region, adr=lora_adr)

        # Restore LoRa state from NVRAM after waking up from DEEPSLEEP.
        # Otherwise, reset LoRa NVRAM and rejoin.
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
            import machine
            # Restore LoRaWAN status after wake up from deep sleep
            if machine.reset_cause() == machine.DEEPSLEEP_RESET:
                self.lora.nvram_restore()
                log.info('[LoRa] LoRaWAN state restored from NVRAM after deep sleep')
            # Otherwise reset LoRaWAN status and deep sleep interval from NVRAM
            else:
                self.lora.nvram_erase()
                log.info('[LoRa] LoRaWAN state erased from NVRAM. Rejoin forced')

                if platform_info.vendor == platform_info.MICROPYTHON.Pycom:
                    import pycom
                    nvram_get   = pycom.nvs_get
                    nvram_erase = pycom.nvs_erase
                elif platform_info.vendor == platform_info.MICROPYTHON.Vanilla:
                    import esp32
                    nvram_get   = esp32.nvs_get
                    nvram_erase = esp32.nvs_erase

                try:
                    if nvram_get('deepsleep') is not None:
                        nvram_erase('deepsleep')
                        log.info('[LoRa] Deep sleep interval erased from NVRAM. Return to settings value')
                except:
                    pass

        if not self.lora.has_joined():
            import binascii

            # Over-the-Air Activation (OTAA)
            if self.settings.get('networking.lora.activation') == 'otaa':
                app_eui = binascii.unhexlify(self.settings.get('networking.lora.otaa.application_eui'))
                app_key = binascii.unhexlify(self.settings.get('networking.lora.otaa.application_key'))

                log.info('[LoRa] Attaching to the LoRaWAN network using OTAA')
                if self.settings.get('networking.lora.otaa.device_eui') is None:
                    self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
                else:
                    dev_eui = binascii.unhexlify(self.settings.get('networking.lora.otaa.device_eui'))
                    self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=0)

            # Activation by Personalization (ABP)
            elif self.settings.get('networking.lora.activation') == 'abp':
                import struct
                dev_addr = struct.unpack(">l", binascii.unhexlify(self.settings.get('networking.lora.abp.device_address')))[0]
                nwk_swkey = binascii.unhexlify(self.settings.get('networking.lora.abp.network_session_key'))
                app_swkey = binascii.unhexlify(self.settings.get('networking.lora.abp.app_session_key'))

                log.info('[LoRa] Attaching to the LoRaWAN network using ABP')
                self.lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey), timeout=0, dr=0)

    def ensure_connectivity(self):

        self.wait_for_join()

        if self.lora_joined:
            if self.lora_socket is None:
                try:
                    self.create_socket()
                except:
                    log.exception("[LoRa] Could not create LoRa socket")
        else:
            log.error("[LoRa] Could not join network")

    def wait_for_join(self):
        """ wait for device activation to complete """

        self.lora_joined = None
        while not self.lora.has_joined():
            log.info('[LoRa] Not joined yet...')
            time.sleep(self.settings.get('networking.lora.otaa.join_check_interval', 2.5))

        self.lora_joined = self.lora.has_joined()

        if self.lora_joined:
            log.info('[LoRa] Joined successfully')
        else:
            log.info('[LoRa] Failed to join network')

        return self.lora_joined

    def create_socket(self):
        """ Create socket for LoRa communication """

        # create a lora socket
        self.socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        self.socket.settimeout(6.0)

        self.lora_socket = True
        log.info('[LoRa] Socket created')

        return self.lora_socket

    def send(self, payload):
        """
        Send a LoRa packet.
        :param payload:
        """
        self.socket.setblocking(True)

        success = self.socket.send(payload)

        self.socket.setblocking(False)

        self.lora.nvram_save()

        return success

    def receive(self):
        """
        Receive a LoRa packet.
        """

        try:
            rx, port = self.socket.recvfrom(256)
        except socket.timeout:
            log.info('[LoRa] No packet received within receive window')

        if rx:
            log.info('[LoRa] Received: {} on port: {}'.format(rx, port))

        return rx, port


class LoRaDriverDragino:
    """
    LoRa driver for Dragino LoRa/GPS HAT on Raspberry Pi.
    """

    def __init__(self, network_manager, settings):
        self.network_manager = network_manager
        self.settings = settings

        self.dragino = None
        self.setup()

    def setup(self):
        log.info('[LoRa] Setting up LoRa')

        # Monkeypatch SX127x library
        from dragino.SX127x.board_config import BOARD
        BOARD.DIO3 = None

        from dragino.dragino import Dragino, LoRaWANAuthentication, LoRaWANConfig

        # Over-the-Air Activation (OTAA)
        if self.settings.get('networking.lora.activation') == 'otaa':
            lora_auth = LoRaWANAuthentication(auth_mode='OTAA',
                                              deveui=self.settings.get('networking.lora.otaa.device_eui'),
                                              appeui=self.settings.get('networking.lora.otaa.application_eui'),
                                              appkey=self.settings.get('networking.lora.otaa.application_key'))

        # Activation by Personalization (ABP)
        elif self.settings.get('networking.lora.activation') == 'abp':
            lora_auth = LoRaWANAuthentication(auth_mode='ABP',
                                              devaddr=self.settings.get('networking.lora.abp.device_address'),
                                              nwskey=self.settings.get('networking.lora.abp.network_session_key'),
                                              appskey=self.settings.get('networking.lora.abp.app_session_key'))

        lora_config = LoRaWANConfig(auth=lora_auth)
        self.dragino = Dragino(config=lora_config, logging_level=logging.DEBUG)

    def start(self):
        log.info('[LoRa] Starting join')
        self.dragino.join()

    def ensure_connectivity(self):
        while not self.dragino.registered():
            log.info('[LoRa] Waiting for connectivity')
            time.sleep(1)

    def send(self, payload):
        self.dragino.send_bytes(list(payload))
        return len(payload)

    def receive(self):
        return None, None
