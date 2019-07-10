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


# Setup logging.
logging.basicConfig(level=logging.INFO, format='%(asctime)-15s [%(name)-10s] %(levelname)-7s: %(message)s')
log = logging.getLogger(__file__)


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

    def __init__(self, mac_prefix=None, mode=None):
        self.mac_prefix = mac_prefix
        self.mode = mode

    def maintain(self):
        self.mode = DeviceMode.maintenance

    def field(self):
        self.mode = DeviceMode.field

    def pkt_callback(pkt):
        pkt.show()  # debug statement

    def arp_ping(self, destination, delay=0):
        """
        The fastest way to discover hosts on a local
        ethernet network is to use the ARP Ping method.

        -- https://scapy.readthedocs.io/en/latest/usage.html#arp-ping

        :param destination: Network to scan.
        :param delay: How long to delay before starting the network scan.
        """
        time.sleep(delay)
        log.info(f'Sending an ARP ping to {destination} to find devices already connected')

        # "srp" means: Send and receive packets at layer 2.
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=destination), timeout=2, verbose=self.VERBOSITY)
        return ans, unans

    def arp_ping_async(self, destination):
        thread = Thread(target=self.arp_ping, args=(destination,), kwargs={'delay': 0.5})
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
        if pkt[ARP].op == 1:  # who-has (request)
            log.debug(f"Request: {pkt[ARP].hwsrc} / {pkt[ARP].psrc} is asking about {pkt[ARP].pdst}")
        if pkt[ARP].op == 2:  # is-at (response)
            log.debug(f"*Response: {pkt[ARP].hwsrc} has address {pkt[ARP].psrc}")
        #sys.stdout.flush()

    def check_esp32(self, pkt):
        if ARP not in pkt:
            return
        self.arp_display(pkt)
        if pkt[ARP].hwsrc.startswith(self.mac_prefix) and pkt[ARP].psrc != '0.0.0.0':
            member = NetworkMember()
            member.mac = pkt[ARP].hwsrc
            member.ip = pkt[ARP].psrc
            log.info(f'Found device at {member}')
            if self.mode is not None:
                self.toggle_maintenance(member)

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
        log.info(f'Waiting for device with MAC address prefix {self.mac_prefix} to appear on your local network')
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
                    address = f"{thing['addr']}/{thing['netmask']}"
                    address_cidr = str(netaddr.IPNetwork(address).cidr)
                    addresses.append(address_cidr)

    return addresses


def boot_monitor(monitor):
    networks = get_local_networks()
    log.info(f'Local networks: {networks}')

    for network in networks:
        monitor.arp_ping_async(network)

    monitor.arp_monitor()
    return


def run_monitor(mac_prefix, command):
    monitor = NetworkMonitor(mac_prefix=mac_prefix)
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
    mac_prefix = os.getenv('MCU_MAC_PREFIX', '80:7d:3a')
    command = sys.argv[1]
    run_monitor(mac_prefix, command)


#hosts = mon.discover_hosts('192.168.178.0/24')
#log.info(f'Hosts found: {hosts}')
