# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import time
import socket
import machine
import network


class MiniNet:

    def __init__(self):
        print('INFO:  WiFi STA: Starting MiniNet')
        self.station = network.WLAN()

    def connect_wifi(self, ssid, password, timeout=3000):
        """
        https://docs.pycom.io/firmwareapi/pycom/network/wlan/
        https://mike632t.wordpress.com/2017/04/11/connecting-my-wipy-to-my-wifi/
        """

        # Duplicate output on UART
        #uart = machine.UART(0, 115200)
        #os.dupterm(uart)

        # Disable telnet and FTP server before connecting to the network
        #server = network.Server()
        #server.deinit()

        # Connect to WLAN
        print('INFO:  WiFi STA: Scanning for networks')
        #self.station = network.WLAN(mode=network.WLAN.STA)
        try:
            self.station.disconnect()
        except:
            pass

        self.station.mode(network.WLAN.STA)
        nets = self.station.scan()
        ssids = [net.ssid for net in nets]

        print('INFO:  WiFi STA: Networks found {}'.format(ssids))
        for net in nets:
            if net.ssid == ssid:
                print('INFO:  WiFi STA: Connecting to "{}"'.format(ssid))
                self.station.connect(net.ssid, auth=(net.sec, password), timeout=timeout)

                try:
                    while not self.station.isconnected():
                        # Save power while waiting
                        machine.idle()
                        time.sleep_ms(250)
                    print('INFO:  WiFi STA: Connected to "{}"'.format(ssid))

                except Exception as ex:
                    print('ERROR: WiFi STA: Connecting to "{}" failed. Please check SSID and PASSWORD.\n'.format(ssid, ex))
                    break


        # Enable telnet and FTP server with new settings
        #server.init(login=('<user>', '<password>'), timeout=600)

        # Wait 10 seconds before continuing
        #time.sleep(10)

        #while not wlan.isconnected():
        #    time.sleep_ms(50)

        #self.wait_for_nic()

        if self.station.isconnected():
            print('INFO:  WiFi STA: Network configuration is {}'.format(self.station.ifconfig()))
            print('INFO:  Ready.')
            print()
            print('INFO:  WiFi STA: IP address is {}'.format(self.get_ip_address()))

        print()
        print('Note: Press CTRL+X or Ctrl+] to detach from the REPL')

    def wait_for_nic(self, retries=5):
        attempts = 0
        while attempts < retries:
            try:
                socket.getaddrinfo("localhost", 333)
                break
            except OSError as ex:
                print('Network interface not available: {}'.format(ex))
            print('Waiting for network interface')
            # Save power while waiting.
            machine.idle()
            time.sleep(0.25)
            attempts += 1
        print('Network interface ready')

    def get_ip_address(self):
        return self.station.ifconfig()[0]
