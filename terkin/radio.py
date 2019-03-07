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

    def __init__(self, wifi_networks):
        self.wifi_networks = wifi_networks
        self.station = None

    def start_wifi(self):
        """
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

        print("WiFi STA: Starting connection")
        self.station.mode(WLAN.STA)

        available_nets = self.station.scan()
        nets = frozenset([e.ssid for e in available_nets])

        known_nets_names = frozenset([e[0] for e in self.wifi_networks])
        net_to_use = list(nets & known_nets_names)

        try:
            net_to_use = net_to_use[0]
            pwd = dict(self.wifi_networks)[net_to_use]
            sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
            print('WiFi STA: Connecting to network "{}"'.format(net_to_use))
            success = self.station.connect(net_to_use, (sec, pwd), timeout=15000)

            # FIXME: Apply timeout
            while not self.station.isconnected():
                # Save power while waiting
                machine.idle()

            print('WiFi STA: Succeeded')

            # Inform about networking status.
            self.print_status()

            return True

        except Exception as ex:
            print("WiFi STA: Connect failed: {}. Switching to AP mode.".format(ex))
            print(WLAN.AP, original_ssid, original_auth, WLAN.INT_ANT)
            # TOOD: Make default channel configurable
            self.station.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)

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
