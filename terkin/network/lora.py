# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import binascii
import socket
import machine
from terkin import logging

log = logging.getLogger(__name__)


class LoRaManager:
    """ """

    def __init__(self, manager, settings):
        self.manager = manager
        self.settings = settings

        # LoRa settings.
        self.otaa_settings = self.settings.get('networking.lora.otaa')
        #self.generated_device_eui = binascii.hexlify(LoRa().mac())

    def start(self):
        """ """
        self.start_lora_join()

    def start_lora_join(self):
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

        # restore LoRa state from NVRAM after waking up from DEEPSLEEP. Reset LoRa NVRAM and rejoin otherwise
        if machine.reset_cause() == machine.DEEPSLEEP_RESET:
            self.lora.nvram_restore()
            log.info('[LoRa] LoRaWAN state restored from NVRAM after deep sleep')
        else:
            self.lora.nvram_erase()
            log.info('[LoRa] LoRaWAN state erased from NVRAM. Rejoin forced')

        # Create LoRaWAN OTAA connection to TTN.
        app_eui = binascii.unhexlify(self.otaa_settings['application_eui'])
        app_key = binascii.unhexlify(self.otaa_settings['application_key'])

        if not self.lora.has_joined():
            log.info('[LoRa] joining the network...')
            if self.otaa_settings.get('device_eui') is None:
                self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
            else:
                dev_eui = binascii.unhexlify(self.otaa_settings['device_eui'])
                self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

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
            log.info('[LoRa] joined...')
        else:
            log.info('[LoRa] did not join in %s attempts', attempts)

        return self.lora_joined

    def create_lora_socket(self):
        """ """

        # create a lora socket
        self.socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # make the socket non-blocking
        self.socket.setblocking(False)

        self.lora_socket = True
        log.info('[LoRa] socket created')

        return self.lora_socket

    def lora_send(self, payload):
        """

        :param payload: 

        """
        success = self.socket.send(payload)

        # give LoRa stack some rest before saving status to NVRAM
        time.sleep(4)
        self.lora.nvram_save()

        return success

    def lora_receive(self):
        """ """
        rx, port = self.socket.recvfrom(256)
        if rx:
            log.info('[LoRa] Received: {}, on port: {}'.format(rx, port))
        time.sleep(6)

        return rx, port
