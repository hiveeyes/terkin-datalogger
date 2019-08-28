# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import machine
import binascii
from network import WLAN
from terkin import logging
from terkin.util import format_mac_address, backoff_time, Stopwatch

log = logging.getLogger(__name__)


class WiFiManager:

    def __init__(self, manager, settings):
        self.manager = manager
        self.settings = settings

        # WIFI settings.
        self.stations = self.settings.get('networking.wifi.stations')
        self.station = None

        # Stopwatch for keeping track of time.
        log.info('Starting stopwatch')
        self.stopwatch = Stopwatch()
        log.info('Started stopwatch successfully')

    def start(self):

        # Todo: Propagate more parameters here, e.g. for using an external antenna.
        self.station = WLAN()

        self.start_interface()

        try:
            import _thread
            _thread.start_new_thread(self.stay_connected, ())
        except ImportError:
            self.connect_once()

    def start_interface(self):
        """
        https://docs.pycom.io/tutorials/all/wlan.html
        https://github.com/pycom/pydocs/blob/master/firmwareapi/pycom/network/wlan.md
        """

        #if machine.reset_cause() == machine.SOFT_RESET:
        #   print("WiFi STA: Network connection after SOFT_RESET.")
        #    self.print_short_status()
        #    # Inform about networking status.
        #    self.print_address_status()
        #    return True

        # Save the default ssid and auth for restoring AP mode later
        #original_ssid = self.station.ssid()
        #original_auth = self.station.auth()

        # Inform about networking status.
        self.print_address_status()

        # Setup network interface.
        log.info("WiFi STA+AP: Starting interface")
        self.station.mode(WLAN.STA_AP)
        self.station.init()

        # Check WiFi connectivity.
        if self.is_connected():

            log.info("WiFi STA: Network connection already established, will skip scanning and resume connectivity.")
            self.print_short_status()

            # Give system some breath.
            time.sleep(0.25)

            # Inform about networking status.
            self.print_short_status()
            self.print_address_status()

            return True

    def enable_ap(self):
        # Todo: Reenable WiFi AP mode in the context of an "initial configuration" mode.
        """
        log.info('WiFi: Switching to AP mode')
        # WLAN.AP, original_ssid, original_auth, WLAN.INT_ANT
        # TOOD: Make default channel configurable
        self.station.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
        """
        pass

    def connect_once(self):

        # Prepare information about known WiFi networks.
        networks_known = frozenset([station['ssid'] for station in self.stations])

        try:
            self.connect_stations(networks_known)

        except:
            log.exception('WiFi STA: Connecting to configured networks "{}" failed'.format(list(networks_known)))

    def stay_connected(self):

        # Prepare information about known WiFi networks.
        networks_known = frozenset([station['ssid'] for station in self.stations])

        # Attempt to connect to known/configured networks.
        attempt = 0
        while True:

            delay = 1

            if self.is_connected():
                attempt = 0

            else:
                log.info("WiFi STA: Connecting to configured networks: %s. Attempt: #%s", list(networks_known), attempt + 1)
                try:
                    self.connect_stations(networks_known)

                except:
                    log.exception('WiFi STA: Connecting to configured networks "{}" failed'.format(list(networks_known)))
                    delay = backoff_time(attempt, minimum=1, maximum=600)
                    log.info('WiFi STA: Retrying in {} seconds'.format(delay))

                attempt += 1

            machine.idle()
            time.sleep(delay)

    def is_connected(self):
        try:
            # ``isconnected()`` returns True when connected to a WiFi access point *and* having a valid IP address.
            if self.station is not None and self.station.isconnected():
                ssid = self.get_ssid()
                if ssid[0] is not None:
                    ip_address = self.get_ip_address()
                    if ip_address is not None and ip_address != '0.0.0.0':
                        return True

        except:
            log.exception('Invoking "is_connected" failed')

        return False

    def power_off(self):
        """
        Power off all radio peripherals.

        - https://forum.pycom.io/topic/563/disabling-wifi-on-lopy
        - https://github.com/Hiverize/FiPy/commit/b6b15677
        """

        # WiFi
        if self.station:
            try:
                log.info('Turning off WiFi')
                self.station.deinit()
            except:
                log.exception('Turning off WiFi failed')

    def connect_stations(self, network_names):

        # Prepare information about known WiFi networks.
        network_map = {station['ssid']: station for station in self.stations}

        for network_name in network_names:
            try:
                # All the configuration details for this network.
                # {
                #    'ssid': 'FooBar',
                #    'password': 'SECRET',
                #    'ifconfig': ('192.168.42.42', '255.255.255.0', '192.168.42.1', '192.168.42.1'),
                # }
                network_selected = network_map[network_name]
                if self.connect_station(network_selected):
                    break

            except Exception:
                log.exception('WiFi STA: Connecting to "{}" failed'.format(network_name))

        if not self.is_connected():

            self.forget_network(network_name)

            message = 'WiFi STA: Connecting to any network candidate failed'
            description = 'Please check your WiFi configuration for one of the ' \
                          '{} station candidates.'.format(len(network_names))
            log.error('{}. {}'.format(message, description))
            log.warning('Todo: We might want to buffer telemetry data to '
                        'flash memory to be scheduled for transmission later.')

            raise WiFiException(message)

    def connect_station(self, network):

        network_name = network['ssid']

        log.info('WiFi STA: Getting auth mode for network "{}"'.format(network_name))

        auth_mode = self.get_auth_mode(network_name)

        log.info('WiFi STA: Preparing connection to network "{}" with auth mode "{}"'.format(network_name, auth_mode))

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

        # Obtain timeout value.
        network_timeout = network.get('timeout', 15.0)

        # Connect to WiFi station.
        log.info('WiFi STA: Starting connection to "{}" with timeout of {} seconds'.format(network_name, network_timeout))
        self.station.connect(network_name, (auth_mode, password), timeout=int(network_timeout * 1000))

        # Wait for network to arrive.
        self.wait_for_connection(network_timeout)

        if not self.is_connected():
            raise WiFiException('WiFi STA: Unable to connect to "{}"'.format(network_name))

        # Inform about networking status.
        self.print_short_status()
        self.print_address_status()

        return True

    def wait_for_connection(self, timeout=15.0):
        """
        Wait for network to arrive.
        """

        # Set interval how often to poll for WiFi connectivity.
        network_poll_interval = 250

        # How many checks to make.
        checks = int(timeout / (network_poll_interval / 1000.0))

        self.stopwatch.reset()

        do_report = True
        while not self.is_connected():

            delta = self.stopwatch.elapsed()
            eta = timeout - delta

            if checks <= 0 or eta <= 0:
                break

            # Report about the progress each 3 seconds.
            if int(delta) % 3 == 0:
                if do_report:
                    log.info('WiFi STA: Waiting for network to come up within {} seconds'.format(eta))
                    do_report = False
            else:
                do_report = True

            # Save power while waiting.
            machine.idle()

            # Don't busy-wait.
            time.sleep_ms(network_poll_interval)

            checks -= 1

    def scan_stations(self):

        # Inquire visible networks.
        log.info("WiFi STA: Scanning for networks")
        try:
            stations_available = self.station.scan()
        except OSError as ex:
            if 'Scan operation Failed' in str(ex):
                log.exception('WiFi STA: Scanning for networks failed')
                self.station.init()

        # Collect SSIDs of available stations.
        networks_found = frozenset([e.ssid for e in stations_available])

        # Print names/SSIDs of networks found.
        log.info("WiFi STA: Networks available: %s", list(networks_found))

        return stations_available

    def get_ssid(self):
        return self.station.ssid()

    def get_ip_address(self):
        try:
            return self.station.ifconfig()[0]
        except:
            log.exception('Unable to get device ip address')

    def get_auth_mode(self, network_name):

        # NVRAM key for storing auth mode per network. Maximum of 15 characters.
        auth_mode_nvs_key = self.auth_mode_nvs_key(network_name)

        # Get WiFi STA auth mode from NVRAM.
        try:
            import pycom
            auth_mode = pycom.nvs_get(auth_mode_nvs_key)
            log.info('WiFi STA: Auth mode from NVRAM with key=%s, value=%s', auth_mode_nvs_key, auth_mode)
        except:
            auth_mode = None

        # Fall back to find out WiFi STA auth mode by network scan.
        if auth_mode is None:
            log.info('WiFi STA: Unknown auth mode for network "%s", invoking WiFi scan', network_name)
            wifi_neighbourhood = self.scan_stations()

            #log.info('WiFi STA: Neighbourhood is %s', wifi_neighbourhood)
            for e in wifi_neighbourhood:
                if e.ssid == network_name:
                    auth_mode = e.sec
                    break

            if not auth_mode:
                message = 'WiFi STA: Unable to inquire auth mode for network "{}"'.format(network_name)
                log.warning(message)
                raise WiFiException(message)

            log.info('WiFi STA: Storing auth mode into NVRAM with key=%s, value=%s', auth_mode_nvs_key, auth_mode)
            try:
                import pycom
                pycom.nvs_set(auth_mode_nvs_key, auth_mode)
            except:
                log.exception('WiFi STA: Storing auth mode into NVRAM failed')

        return auth_mode

    def auth_mode_nvs_key(self, ssid):
        """
        Hack to get a short representation of a WiFi SSID in order to
        squeeze it into a NVRAM key with a maximum length of 15 characters.

        Fixme: Review this.
        """
        import hashlib
        import ubinascii
        digest = ubinascii.hexlify(hashlib.sha512(ssid).digest()).decode()
        identifier = 'wa.{}'.format(digest[15:27])
        return identifier

    def forget_network(self, network_name):
        log.info('WiFi STA: Forgetting NVRAM data for network "{}"'.format(network_name))
        auth_mode_nvs_key = self.auth_mode_nvs_key(network_name)
        try:
            import pycom
            pycom.nvs_erase(auth_mode_nvs_key)
        except:
            pass

    def print_short_status(self):
        log.info('WiFi STA: Connected to "{}" with IP address "{}"'.format(self.get_ssid(), self.get_ip_address()))

    def print_address_status(self):
        mac_address = self.humanize_mac_addresses(self.station.mac())
        ifconfig = self.station.ifconfig()
        log.info('WiFi STA: Networking address (MAC): %s', mac_address)
        log.info('WiFi STA: Networking address (IP):  %s', ifconfig)

    def humanize_mac_addresses(self, mac):
        info = {}
        if hasattr(mac, 'sta_mac'):
            info['sta_mac'] = format_mac_address(binascii.hexlify(mac.sta_mac).decode())
        if hasattr(mac, 'ap_mac'):
            info['ap_mac'] = format_mac_address(binascii.hexlify(mac.ap_mac).decode())
        return info

    def print_metrics(self):
        metrics = SystemWiFiMetrics(self.station).read()
        log.info('WiFi STA: Metrics: %s', metrics)


class WiFiException(Exception):
    pass


class SystemWiFiMetrics:

    def __init__(self, station):
        self.station = station

    def read(self):

        if self.station is None:
            return

        stats = {
            'system.wifi.bandwidth': self.station.bandwidth(),
            'system.wifi.channel': self.station.channel(),
            #'system.wifi.protocol': self.station.wifi_protocol(),
            'system.wifi.max_tx_power': self.station.max_tx_power(),
            #'system.wifi.joined_ap_info': self.station.joined_ap_info(),
        }

        try:
            stats['system.wifi.country'] = self.station.country().country
        except:
            pass

        try:
            stats['system.wifi.rssi'] = self.station.joined_ap_info().rssi
        except:
            pass

        return stats
