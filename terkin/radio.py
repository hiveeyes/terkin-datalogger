# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import socket
import binascii
import machine
from network import WLAN
from terkin import logging


# TODO: What about when coming back from sleep?
# Needed to avoid losing connection after a soft reboot
# if True or machine.reset_cause() != machine.SOFT_RESET:
import pycom

from terkin.util import format_exception

log = logging.getLogger(__name__)


class WiFiException(Exception):
    pass


class NetworkManager:

    def __init__(self, settings):
        self.settings = settings
        """ WIFI settings """
        self.stations = self.settings.get('networking.wifi.stations')
        self.stations_available = []
        self.station = None

        """ LoRa settings """
        self.otaa_settings = self.settings.get('networking.lora.otaa')
        #self.generated_device_eui = binascii.hexlify(LoRa().mac())

    def start_wifi(self):
        """
        https://docs.pycom.io/tutorials/all/wlan.html
        https://github.com/pycom/pydocs/blob/master/firmwareapi/pycom/network/wlan.md
        """
        self.station = WLAN()

        #if machine.reset_cause() == machine.SOFT_RESET:
        #   print("WiFi STA: Network connection after SOFT_RESET.")
        #    self.print_short_status()
        #    # Inform about networking status.
        #    self.print_address_status()
        #    return True

        # Save the default ssid and auth for restoring AP mode later
        original_ssid = self.station.ssid()
        original_auth = self.station.auth()

        # Setup network interface.
        self.station.init()

        # Check WiFi connectivity.
        if self.station.isconnected():

            log.info("WiFi STA: Network connection already established, will skip scanning and resume connectivity.")
            self.print_short_status()

            # Give system some breath.
            time.sleep(0.25)

            # Inform about networking status.
            self.print_address_status()

            return True

        # Prepare information about known WiFi networks.
        network_map = {station['ssid']: station for station in self.stations}
        networks_known = frozenset(network_map.keys())

        log.info("WiFi STA: Networks configured: %s", list(networks_known))

        log.info("WiFi STA: Starting interface")
        self.station.mode(WLAN.STA)

        # Names/SSIDs of networks found.
        log.info("WiFi STA: Scanning for networks")
        self.stations_available = self.station.scan()
        networks_found = frozenset([e.ssid for e in self.stations_available])
        log.info("WiFi STA: Networks available: %s", list(networks_found))

        # Compute set of effective networks by intersecting known with found ones.
        network_candidates = list(networks_found & networks_known)
        log.info("WiFi STA: Network candidates: %s", network_candidates)

        for network_name in network_candidates:
            try:
                # All the configuration details for this network.
                # {
                #    'ssid': 'FooBar',
                #    'password': 'SECRET',
                #    'ifconfig': ('192.168.42.42', '255.255.255.0', '192.168.42.1', '192.168.42.1'),
                # }
                network_selected = network_map[network_name]
                if self.wifi_connect_station(network_selected):
                    break

            except WiFiException:
                log.exception('WiFi STA: Connecting to "{}" failed'.format(network_name))

        if not self.station.isconnected():
            message = 'WiFi STA: Connecting to any network candidate failed'
            description = 'Please check your WiFi configuration for one of the ' \
                          '{} station candidates in your neighbourhood.'.format(len(network_candidates))
            log.error('{}. {}'.format(message, description))
            log.warning('Todo: We might want to switch to AP mode here or alternatively '
                        'buffer telemetry data to flash to be scheduled for transmission later.')
            raise WiFiException(message)

        # TODO: Reenable WiFi AP mode in the context of an "initial configuration" mode.
        """
        log.info('WiFi: Switching to AP mode')
        # WLAN.AP, original_ssid, original_auth, WLAN.INT_ANT
        # TOOD: Make default channel configurable
        self.station.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
        """

    def wifi_connect_station(self, network):

        network_name = network['ssid']

        log.info('WiFi STA: Attempting to connect to network "{}"'.format(network_name))

        auth_mode = [e.sec for e in self.stations_available if e.ssid == network_name][0]
        password = network['password']

        # TODO: Optionally, configure hostname.
        # https://docs.micropython.org/en/latest/library/network.WLAN.html
        # https://github.com/pycom/pycom-micropython-sigfox/pull/165
        # https://forum.pycom.io/topic/3326/new-firmware-release-v1-18-0
        if 'dhcp_hostname' in network:
            if hasattr(self.station, 'config'):
                log.ingo('WiFi STA: Using dhcp_hostname "{}"'.format(network['dhcp_hostname']))
                self.station.config(dhcp_hostname=network['dhcp_hostname'])
            else:
                log.error('Could not set hostname on older MicroPython')

        # Optionally, configure static IP address.
        if 'ifconfig' in network:
            log.info('WiFi STA: Using static network configuration "{}"'.format(network_name))
            self.station.ifconfig(config=network['ifconfig'])

        # Connect to WiFi station.
        log.info('WiFi STA: Connecting to "{}"'.format(network_name))
        self.station.connect(network_name, (auth_mode, password), timeout=self.settings.get('networking.wifi.timeout'))

        # FIXME: If no known network is found, the program will lockup here.
        # ``isconnected()`` returns True when connected to a WiFi access point and having a valid IP address.
        nic_retries = 15
        while not self.station.isconnected() and nic_retries > 0:
            log.info('WiFi STA: Waiting for network "{}".'.format(network_name))
            time.sleep(1)
            nic_retries -= 1
            # Save power while waiting
            machine.idle()

        if not self.station.isconnected():
            raise WiFiException('WiFi STA: Unable to connect to "{}"'.format(network_name))

        # Inform about networking status.
        self.print_short_status()
        self.print_address_status()

        return True

    def get_ssid(self):
        return self.station.ssid()

    def get_ip_address(self):
        try:
            return self.station.ifconfig()[0]
        except:
            pass

    def print_address_status(self):
        mac_address = self.station.mac()
        ifconfig = self.station.ifconfig()
        log.info('WiFi STA: Networking address: mac={}, ifconfig={}'.format(mac_address, ifconfig))

    def print_short_status(self):
        log.info('WiFi STA: Connected to "{}" with IP address "{}"'.format(self.get_ssid(), self.get_ip_address()))

    def wait_for_nic(self, retries=5):
        attempts = 0
        while attempts < retries:
            try:
                socket.getaddrinfo("localhost", 333)
                break
            except OSError as ex:
                log.warning('Network interface not available: %s', format_exception(ex))
            log.info('Waiting for network interface')
            time.sleep(0.25)
            attempts += 1
        log.info('Network interface ready')

    def start_lora(self):
        self.start_lora_join()
        self.wait_for_lora_join(42)

        time.sleep(2.5)

        if self.lora_joined:
            self.create_lora_socket()
        else:
            log.error("[LoRa] Could not join network")

    def start_lora_join(self):

        from network import LoRa

        #pycom.rgbled(0x0f0000) # red
        #self.lora = LoRa(mode=LoRa.LORAWAN, region=self.otaa_settings['region'])
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

        # Create LoRaWAN OTAA connection to TTN.
        app_eui = binascii.unhexlify(self.otaa_settings['application_eui'])
        app_key = binascii.unhexlify(self.otaa_settings['application_key'])

        # Remark: For Pycom Nanogateway.
        # Set the 3 default channels to the same frequency (must be before sending the otaa join request)
        #self.lora.add_channel(0, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)
        #self.lora.add_channel(1, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)
        #self.lora.add_channel(2, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)

        if self.otaa_settings.get('device_eui') is None:
            self.lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)
        else:
            dev_eui = binascii.unhexlify(self.otaa_settings['device_eui'])
            self.lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)

    def wait_for_lora_join(self, attempts):
        self.lora_joined = None
        for i in range(0, attempts):
            while not self.lora.has_joined():
                time.sleep(2.5)
                #pycom.rgbled(0x0f0f00) # yellow
                time.sleep(0.1)
                log.info('[LoRA] Not joined yet...')
                #pycom.rgbled(0x000000) # off

        self.lora_joined = self.lora.has_joined()

        if self.lora_joined:
            log.info('[LoRA] joined...')
        else:
            log.info('[LoRa] did not join in %s attempts', attempts)

        #for i in range(3, 16):
        #    self.lora.remove_channel(i)

        return self.lora_joined

    def create_lora_socket(self):
        # create a lora socket

        self.lora_socket = None
        self.socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        #self.socket.setsockopt(socket.SOL_LORA, socket.SO_DR, self.otaa_settings['datarate'])
        self.socket.setsockopt(socket.SOL_LORA, socket.SO_DR, self.otaa_settings['datarate'])
        # make the socket non-blocking
        self.socket.setblocking(False)

        self.lora_socket = True
        log.info('[LoRa] socket created')

        for i in range(0,2):
            #pycom.rgbled(0x000f00) # green
            time.sleep(0.1)
            #pycom.rgbled(0x000000) # off

        time.sleep(4.0)
        return self.lora_socket

    def lora_send(self, payload):
        success = self.socket.send(payload)
        for i in range(0,2):
            #pycom.rgbled(0x00000f) # green
            time.sleep(0.1)
            #pycom.rgbled(0x000000) # off

        return success

    def lora_receive(self):
        rx, port = self.socket.recvfrom(256)
        if rx:
            #pycom.rgbled(0x000f00) # green
            log.info('[LoRa] Received: {}, on port: {}'.format(rx, port))
            #pycom.rgbled(0x000f00) # green
        time.sleep(6)

        return rx, port
