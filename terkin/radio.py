# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time

import machine
import usocket as socket
from network import WLAN, LoRa
import binascii
import socket
import pycom


# TODO: What about when coming back from sleep?
# Needed to avoid losing connection after a soft reboot
# if True or machine.reset_cause() != machine.SOFT_RESET:
import pycom

class NetworkManager:

    def __init__(self, settings):
        self.settings = settings
        """ WIFI settings """
        self.stations = self.settings.get('networking.wifi.stations')
        self.stations_available = []
        self.station = None

        """ LoRa settings """
        self.otaa_settings = self.settings.get('networking.lora.otaa')

    def start_wifi(self):
        """
        https://docs.pycom.io/tutorials/all/wlan.html
        https://github.com/pycom/pydocs/blob/master/firmwareapi/pycom/network/wlan.md
        """
        self.station = WLAN()

        # Save the default ssid and auth for restoring AP mode later
        original_ssid = self.station.ssid()
        original_auth = self.station.auth()

        # Setup network interface.
        self.station.init()

        # Check WiFi connectivity.
        if self.station.isconnected():

            print("WiFi STA: Already connected")

            # Give system some breath.
            time.sleep(0.25)

            # Inform about networking status.
            self.print_status()

            return True

        # Prepare information about known WiFi networks.
        network_map = {station['ssid']: station for station in self.stations}
        networks_known = frozenset(network_map.keys())

        print("WiFi STA: Starting connection")
        self.station.mode(WLAN.STA)

        # Names/SSIDs of networks found.
        print("WiFi STA: Scanning for networks")
        self.stations_available = self.station.scan()
        networks_found = frozenset([e.ssid for e in self.stations_available])
        print("WiFi STA: Available networks: {}".format(networks_found))

        # Compute set of effective networks by intersecting known with found ones.
        network_candidates = list(networks_found & networks_known)

        for network_name in network_candidates:
            try:
                # All the configuration details for this network.
                # {
                #    'ssid': 'FooBar',
                #    'password': 'SECRET',
                #    'ifconfig': ('192.168.42.42', '255.255.255.0', '192.168.42.1', '192.168.42.1'),
                # }
                network_selected = network_map[network_name]
                self.wifi_connect_station(network_selected)

            except Exception as ex:
                print('WiFi STA: Connecting to "{}" failed.'.format(network_name, ex))

        """
        print('WiFi: Switching to AP mode. {}'.format(network_name, ex))
        print(WLAN.AP, original_ssid, original_auth, WLAN.INT_ANT)
        # TOOD: Make default channel configurable
        self.station.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
        """

    def wifi_connect_station(self, network):

        network_name = network['ssid']

        print('WiFi STA: Attempting to connect to network "{}"'.format(network_name))

        auth_mode = [e.sec for e in self.stations_available if e.ssid == network_name][0]
        password = network['password']

        # Optionally, configure static IP address.
        if 'ifconfig' in network:
            print('WiFi STA: Using static network configuration "{}"'.format(network_name))
            self.station.ifconfig(config=network['ifconfig'])

        # Connect to WiFi station.
        print('WiFi STA: Connecting to "{}"'.format(network_name))
        self.station.connect(network_name, (auth_mode, password), timeout=self.settings.get('networking.wifi.timeout'))

        # FIXME: If no known network is found, the program will lockup here.
        # ``isconnected()`` returns True when connected to a WiFi access point and having a valid IP address.
        retries = 5
        while not self.station.isconnected() and retries > 0:
            print('WiFi STA: Waiting for network "{}".'.format(network_name))
            time.sleep(1)
            retries -= 1
            # Save power while waiting
            #machine.idle()

        if not self.station.isconnected():
            raise TimeoutError('Unable to connect to WiFi station "{}"'.format(network_name))

        print('WiFi STA: Connected to "{}" with IP address "{}"'.format(network_name, self.station.ifconfig()[0]))

        # Inform about networking status.
        self.print_status()

        return True

    def print_status(self):
        mac_address = self.station.mac()
        ifconfig = self.station.ifconfig()
        status = None
        # status = self.station.status()
        #print(dir(self.station))
        print('Networking status: mac={}, ifconfig={}, status={}'.format(mac_address, ifconfig, status))

    def wait_for_nic(self, retries=5):
        attempts = 0
        while attempts < retries:
            try:
                socket.getaddrinfo("localhost", 333)
                break
            except OSError as ex:
                print(ex)
            print('Waiting for networking')
            time.sleep(0.25)
            attempts += 1
        print('Networking established')

    def start_lora(self):
        pycom.rgbled(0x0f0000) # red
        #self.lora = LoRa(mode=LoRa.LORAWAN, region=self.otaa_settings['region'])
        self.lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

        # create an OTA authentication params
        self.dev_eui = binascii.unhexlify(self.otaa_settings['device_eui']) # these settings can be found from TTN
        self.app_eui = binascii.unhexlify(self.otaa_settings['application_eui']) # these settings can be found from TTN
        self.app_key = binascii.unhexlify(self.otaa_settings['application_key']) # these settings can be found from TTN

        # set the 3 default channels to the same frequency (must be before sending the otaa join request)
        self.lora.add_channel(0, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)
        self.lora.add_channel(1, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)
        self.lora.add_channel(2, frequency=self.otaa_settings['frequency'], dr_min=0, dr_max=5)

        self.lora.join(activation=LoRa.OTAA, auth=(self.otaa_settings['device_eui'], self.otaa_settings['application_eui'], self.otaa_settings['application_key']), timeout=0, dr=self.otaa_settings['datarate'])


    def wait_for_lora_join(self, attempts):
        self.lora_joined = None
        for i in range(0, attempts):
            while not self.lora.has_joined():
                time.sleep(2.5)
                pycom.rgbled(0x0f0f00) # yellow
                time.sleep(0.1)
                print('[LoRA] Not joined yet...')
                pycom.rgbled(0x000000) # off

        self.lora_joined = self.lora.has_joined()

        if self.lora_joined:
            print('[LoRA] joined...')
        else:
            print('[lora] did not join in', attempts,'attempts')

        for i in range(3, 16):
            self.lora.remove_channel(i)

        return self.lora_joined

    def create_lora_socket(self):
        # create a lora socket

        self.lora_socket = None
        self.socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

        # set the LoRaWAN data rate
        self.socket.setsockopt(socket.SOL_LORA, socket.SO_DR, self.otaa_settings['datarate'])

        # make the socket non-blocking
        self.socket.setblocking(False)

        self.lora_socket = True
        print('[lora] socket created')

        for i in range(0,2):
            pycom.rgbled(0x000f00) # green
            time.sleep(0.1)
            pycom.rgbled(0x000000) # off

        #time.sleep(5.0)
        return self.lora_socket

    def lora_send(self, payload):
        payload_send = None
        self.socket(payload) 
        payload_send = True
        for i in range(0,2):
            pycom.rgbled(0x00000f) # green
            time.sleep(0.1)
            pycom.rgbled(0x000000) # off

        return payload_send

    def lora_receive(self):
        rx, port = self.socket.recvfrom(256)
        if rx:
            pycom.rgbled(0x000f00) # green
            print('Received: {}, on port: {}'.format(rx, port))
            pycom.rgbled(0x000f00) # green
        time.sleep(6)

        return rx, port

