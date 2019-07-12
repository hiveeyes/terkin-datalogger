# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import time
import socket
import logging
from threading import Thread

import netaddr
import netifaces

from scapy.all import Ether, ARP, srp, sniff

"""
Backlog
=======

- Operate on multiple devices.
- Add more MAC address prefixes from the Pycom device family.
- Acknowledge UDP mode change to improve user feedback.
- Honor KeyboardInterrupt / CTRL+C on Windows.
- Lower-case MAC addresses before comparison.

"""

# Setup logging.
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s [%(name)-10s] %(levelname)-7s: %(message)s')
log = logging.getLogger(__file__)
#log.setLevel(logging.DEBUG)


class NetworkWatch:

    # Configuration settings.
    HOSTNAME = 'espressif'
    INTERVAL = 1.0

    def wait_hostname(self, hostname):
        hostname = hostname or self.HOSTNAME
        waiting = False
        count = 0
        while True:
            try:
                ip_address = socket.gethostbyname(hostname)
                if waiting:
                    sys.stderr.write('\n')
                log.info(f'Hostname "{hostname}" found at IP address "{ip_address}"')
                return ip_address

            except socket.gaierror as ex:
                #print('ex:', ex, dir(ex))
                if ex.errno == 8:
                    pass
                else:
                    raise

            if waiting:
                sys.stderr.write('.')
                if count % 79 == 0:
                    sys.stderr.write('\n')
                sys.stderr.flush()

            else:
                waiting = True
                log.info(f'Waiting for hostname "{hostname}" to appear on your local network')

            count +=1
            time.sleep(self.INTERVAL)

    def wait_hostname_forever(self, hostname=None):
        hostname = hostname or self.HOSTNAME
        while True:
            try:
                ip_address = self.wait_hostname(hostname)
            except Exception as ex:
                log.exception(f'Attempt to wait for hostname "{hostname} failed')
            time.sleep(1)


class NetworkMember:

    def __init__(self):
        self.mac = None
        self.ip = None
        #self.host = None

    def __repr__(self):
        return str(self.__dict__)


class DeviceMode:
    maintenance = 1
    field = 2


class NetworkMonitor:

    VERBOSITY = 0
    TRACE = False

    def __init__(self, mac_prefixes=None, mode=None):
        self.mac_prefixes = mac_prefixes
        self.mode = mode

    def maintain(self):
        self.mode = DeviceMode.maintenance

    def field(self):
        self.mode = DeviceMode.field

    def pkt_callback(pkt):
        pkt.show()  # debug statement

    def arp_ping(self, destination):
        """
        The fastest way to discover hosts on a local
        ethernet network is to use the ARP Ping method.

        -- https://scapy.readthedocs.io/en/latest/usage.html#arp-ping

        :param destination: Network to scan.
        :param delay: How long to delay before starting the network scan.
        """
        log.info(f'Sending ARP ping request to {destination}')
        # "srp" means: Send and receive packets at layer 2.
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=destination), timeout=5, verbose=self.VERBOSITY)
        return ans, unans

    def arp_discover(self, destination, delay=0):
        time.sleep(delay)
        return self.arp_ping(destination)

    def arp_discover_background(self, destination):
        thread = Thread(target=self.arp_discover, args=(destination,), kwargs={'delay': 0.5})
        thread.start()
        #thread.join()

    def discover_hosts(self, destination):

        ans, unans = self.arp_ping(destination)

        # Print summary.
        #ans.summary(lambda s: [r.sprintf("%Ether.src% %ARP.psrc%") for r in s])

        members = set()
        for snd, rcv in ans:
            member = NetworkMember()
            member.mac = rcv.sprintf('%Ether.src%')
            member.ip = rcv.sprintf('%ARP.psrc%')
            members.add(member)

        return list(members)

    def arp_monitor_callback(self, pkt):
        if ARP in pkt and pkt[ARP].op in (1, 2):  # who-has or is-at
            print(pkt.sprintf("%ARP.hwsrc% %ARP.psrc%"))
            sys.stdout.flush()

    def arp_display(self, pkt):
        # https://thepacketgeek.com/scapy-sniffing-with-custom-actions-part-1/
        #log.debug('Packet: %s', dir(pkt[ARP]))
        if pkt[ARP].op == 1:  # who-has (request)
            log.debug(f"Request: {pkt[ARP].hwsrc} / {pkt[ARP].psrc} is asking about {pkt[ARP].pdst}")
        if pkt[ARP].op == 2:  # is-at (response)
            log.debug(f"*Response: {pkt[ARP].hwsrc} has address {pkt[ARP].psrc}")
        if self.TRACE:
            pkt[ARP].show()
        sys.stdout.flush()

    def check_esp32(self, pkt):

        # Only process ARP packages.
        if ARP not in pkt:
            return

        # Debugging.
        self.arp_display(pkt)

        # Filter irrelevant devices and addresses.
        if pkt[ARP].psrc == '0.0.0.0' or not self.match_mac_prefix(pkt[ARP].hwsrc):
            return

        member = NetworkMember()
        member.mac = pkt[ARP].hwsrc
        member.ip = pkt[ARP].psrc
        log.info(f'Found device at {member}')
        if self.mode is not None:
            self.toggle_maintenance(member)

    def match_mac_prefix(self, mac_address):
        mac_address = normalize_mac_address(mac_address)
        for prefix in self.mac_prefixes:
            prefix = normalize_mac_address(prefix)
            if mac_address.startswith(prefix):
                return True
        return False

    def arp_monitor(self):
        """
        Simplistic ARP Monitor

        This program uses the sniff() callback (parameter prn). The store
        parameter is set to 0 so that the sniff() function will not store
        anything (as it would do otherwise) and thus can run forever.

        The filter parameter is used for better performances on high load:
        The filter is applied inside the kernel and Scapy will only see ARP traffic.

        -- https://scapy.readthedocs.io/en/latest/usage.html#simplistic-arp-monitor
        """
        log.info(f'Waiting for any devices having MAC address prefixes of {self.mac_prefixes} '
                 f'to appear on your local network')
        #sniff(prn=self.arp_monitor_callback, filter="arp", store=0)
        sniff(prn=self.check_esp32, filter="arp", store=0)

    def toggle_maintenance(self, member):
        # echo 'maintenance.enable()' | ncat --udp 192.168.178.20 666
        port = 666

        log.info(f'Connecting to device mode server at {member.ip}:{port}')
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setblocking(False)
        s.connect((member.ip, port))

        if self.mode == DeviceMode.maintenance:
            log.info(f'Pulling {member.ip} into maintenance mode')
            s.send(b'maintenance.enable()')

        elif self.mode == DeviceMode.field:
            log.info(f'Releasing {member.ip} from maintenance mode')
            s.send(b'maintenance.disable()')


# Utilities

def get_primary_ip():
    # https://stackoverflow.com/a/28950776
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def get_local_networks():
    addresses = []
    for interface in netifaces.interfaces():
        for elem in netifaces.ifaddresses(interface).values():
            for thing in elem:
                #print(thing)
                if 'addr' in thing and 'netmask' in thing and 'broadcast' in thing:

                    # IPv4 address / IPv4 netmask
                    address = f"{thing['addr']}/{thing['netmask']}"

                    if address.startswith('127') or address.startswith('169.254'):
                        continue

                    try:
                        address_cidr = str(netaddr.IPNetwork(address).cidr)
                        addresses.append(address_cidr)

                    except:
                        log.debug(f'Ignoring address {address}. IPv4 only.')

    return addresses


def normalize_mac_address(mac_address):
    return mac_address.lower().replace(':', '')


def str_grouper(n, iterable):
    # https://stackoverflow.com/questions/11006702/elegant-format-for-a-mac-address-in-python-3-2/11006779#11006779
    args = [iter(iterable)] * n
    for part in zip(*args):  # itertools.izip in 2.x for efficiency.
        yield "".join(part)


def format_mac_address(mac_address):
    return ":".join(str_grouper(2, mac_address)).lower()


# Main program

def boot_monitor(monitor):

    networks = get_local_networks()
    log.info(f'IP networks found: {networks}')

    for network in networks:
        log.info(f'Discovering devices already connected to IP network {network}')
        monitor.arp_discover_background(network)

    monitor.arp_monitor()


def run_monitor(command, mac_prefixes):
    monitor = NetworkMonitor(mac_prefixes=mac_prefixes)
    if command == 'maintain':
        monitor.maintain()
    elif command == 'field':
        monitor.field()
    elif command == 'monitor':
        pass
    else:
        log.error(f'Command "{command}" not implemented')
        return

    boot_monitor(monitor)


if __name__ == '__main__':

    # There are different MAC address prefixes for different Pycom devices.
    # Thanks for finding out, @ClemensGruber.
    # WiPy: 30:ae:a4
    # FiPy: 80:7d:3a

    mac_prefixes_default = [
        # WiPy
        '30:ae:a4',
        # FiPy
        '80:7d:3a'
    ]

    # Read command line arguments.
    command = sys.argv[1]
    try:
        mac_prefixes = sys.argv[2].split(',')
    except:
        mac_prefixes = mac_prefixes_default

    mac_prefixes = list(map(format_mac_address, mac_prefixes))

    # Start network monitoring and device discovery machinery.
    run_monitor(command, mac_prefixes)


#hosts = mon.discover_hosts('192.168.178.0/24')
#log.info(f'Hosts found: {hosts}')
