# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time

import machine
import usocket as socket
from network import WLAN


# TODO: What about when coming back from sleep?
# Needed to avoid losing connection after a soft reboot
# if True or machine.reset_cause() != machine.SOFT_RESET:

class NetworkManager:

    def __init__(self, settings):
        self.settings = settings
        self.stations = self.settings.get('networking.wifi.stations')
        self.stations_available = []
        self.station = None

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
