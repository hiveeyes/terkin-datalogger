# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
import machine
import network
import binascii

from terkin import logging
from terkin.sensor.system import AbstractSystemSensor
from terkin.util import get_platform_info, format_mac_address, backoff_time, Stopwatch

log = logging.getLogger(__name__)


class WiFiManager:
    """
    Manages all things relevant to the WiFi connection.
    """

    def __init__(self, manager, settings):

        self.manager = manager
        self.settings = settings

        # WIFI settings.
        self.phy = self.settings.get('networking.wifi.phy', {})
        self.stations = self.settings.get('networking.wifi.stations')
        self.station = None

        # Stopwatch for keeping track of time.
        log.info('Starting stopwatch')
        self.stopwatch = Stopwatch()
        log.info('Started stopwatch successfully')

        # Helper for the ``stay_connected`` thread.
        self.is_running = False

        # Reference to platform information.
        self.platform_info = get_platform_info()

    def start(self):
        """ """

        self.start_interface()

        # Check WiFi connectivity.
        if not self.is_connected():

            # Free up some memory.
            # self.manager.device.run_gc()

            # Connect to WiFi network and wait for successful connection.
            self.connect_once()

        else:

            log.info("WiFi STA: Network connection already established, will skip scanning and resume connectivity.")
            self.print_short_status()

            # Give system some breath.
            #time.sleep(0.25)

            # Inform about networking status.
            #self.print_short_status()
            self.print_address_status()

        # Start thread to monitor WiFi connection and reconnect if required.
        try:
            import _thread
            self.is_running = True
            log.info('Starting WiFi connection monitor')
            _thread.start_new_thread(self.stay_connected_invoke, ())
        except:
            log.warning('Failed starting WiFi connection monitor')

    def stop(self):
        log.info('Shutting down WiFi connection monitor')
        self.is_running = False

    def start_interface(self):
        """
        Genuine MicroPython:
        https://docs.micropython.org/en/latest/library/network.WLAN.html
        
        Pycom MicroPython:
        https://docs.pycom.io/tutorials/all/wlan.html
        https://github.com/pycom/pydocs/blob/master/firmwareapi/pycom/network/wlan.md
        """

        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            self.station = network.WLAN()
        else:
            log.info('WiFi STA: Will exclusively use STA mode on this platform. AP mode not implemented yet.')
            self.station = network.WLAN(network.STA_IF)

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
        log.info("WiFi: Starting interface")

        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            self.configure_antenna()

            # FIXME: Make STA or AP or STA_AP configurable.
            self.station.mode(network.WLAN.STA_AP)

            # Initialize the WiFi peripheral.
            self.station.init()

        else:
            self.station.active(True)

    def configure_antenna(self):
        """ """
        # https://community.hiveeyes.org/t/signalstarke-des-wlan-reicht-nicht/2541/11
        # https://docs.pycom.io/firmwareapi/pycom/network/wlan/

        antenna_external = self.phy.get('antenna_external', False)

        if not hasattr(self.station, 'antenna'):
            # Select antenna, 0=chip, 1=external.
            antenna_value = 0
            if antenna_external:
                antenna_value = 1
            self.station.config(antenna=antenna_value)
            return

        if antenna_external:
            antenna_pin = self.phy.get('antenna_pin')
            log.info('WiFi: Using external antenna on pin %s', antenna_pin)

            # To use an external antenna, set P12 as output pin.
            from machine import Pin
            Pin(antenna_pin, mode=Pin.OUT)(True)

            # Configure external WiFi antenna.
            self.station.antenna(network.WLAN.EXT_ANT)

        else:
            log.info('WiFi: Using internal antenna')
            self.station.antenna(network.WLAN.INT_ANT)

    def enable_ap(self):
        """ """
        # Todo: Reenable WiFi AP mode in the context of an "initial configuration" mode.
        """
        log.info('WiFi: Switching to AP mode')
        # WLAN.AP, original_ssid, original_auth, WLAN.INT_ANT
        # TOOD: Make default channel configurable
        self.station.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
        """
        pass

    def get_configured_stations(self):
        return frozenset([station['ssid'] for station in self.stations])

    def connect_once(self):
        """ """

        # Prepare information about known WiFi networks.
        networks_known = self.get_configured_stations()

        try:
            self.connect_stations(networks_known)

        except Exception as ex:
            log.exc(ex, 'WiFi STA: Connecting to configured networks "{}" failed'.format(list(networks_known)))

    def stay_connected_invoke(self):
        try:
            self.stay_connected()
        except KeyboardInterrupt:
            log.info("Received KeyboardInterrupt within WiFi connection monitor")
            self.stop()
            raise

    def stay_connected(self):
        """ """

        # Prepare information about known WiFi networks.
        networks_known = self.get_configured_stations()

        # Attempt to connect to known/configured networks.
        attempt = 0
        while self.is_running:

            delay = 1

            if self.is_connected():
                attempt = 0

            else:
                log.info("WiFi STA: Connecting to configured networks: %s. "
                         "Attempt: #%s", list(networks_known), attempt + 1)
                try:
                    self.connect_stations(networks_known)

                except KeyboardInterrupt:
                    raise

                except Exception as ex:
                    log.exc(ex, 'WiFi STA: Connecting to configured networks "{}" failed'.format(list(networks_known)))
                    delay = backoff_time(attempt, minimum=1, maximum=600)
                    log.info('WiFi STA: Retrying in {} seconds'.format(delay))

                attempt += 1

            machine.idle()
            time.sleep(delay)

    def is_connected(self):
        """
        Check if connected to WiFi access point and
        connection yielded a valid IP address.
        """
        try:
            # ``isconnected()`` returns True when connected to a
            # WiFi access point *and* having a valid IP address.
            if self.station is not None and self.station.isconnected():
                ssid = self.get_ssid()
                if ssid[0] is not None:
                    ip_address = self.get_ip_address()
                    if ip_address is not None and ip_address != '0.0.0.0':
                        return True

        except Exception as ex:
            if ex.__class__.__name__ != 'TimeoutError':
                log.exc(ex, 'Invoking "isconnected" failed')

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
            except Exception as ex:
                log.exc(ex, 'Turning off WiFi failed')

    def connect_stations(self, network_names):
        """

        :param network_names: 

        """

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

            except Exception as ex:
                log.exc(ex, 'WiFi STA: Connecting to "{}" failed'.format(network_name))

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
        """

        :param network: 

        """

        network_name = network['ssid']

        log.info('WiFi STA: Preparing connection to network "{}"'.format(network_name))

        auth_mode = None
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            log.info('WiFi STA: Getting auth mode')
            auth_mode = self.get_auth_mode(network_name)
            log.info('WiFi STA: Auth mode is "{}"'.format(auth_mode))

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
        # TODO: Make default timeout configurable.
        network_timeout = network.get('timeout', 15.0)

        # Connect to WiFi station.
        log.info('WiFi STA: Starting connection to "{}" '
                 'with timeout of {} seconds'.format(network_name, network_timeout))
        self._connect(network_name, password, auth_mode=auth_mode, timeout=network_timeout)

        # After reset, WiFi regularly does not connect.
        # So, let's just try again working around this weird obstacle.
        self.wait_for_connection(2)
        if not self.is_connected():
            self._connect(network_name, password, auth_mode=auth_mode, timeout=network_timeout)

        # Wait for network to arrive.
        self.wait_for_connection(network_timeout)

        # Finally, check for WiFi connection.
        if not self.is_connected():
            raise WiFiException('WiFi STA: Unable to connect to "{}"'.format(network_name))

        # Inform about networking status.
        self.print_short_status()
        self.print_address_status()

        return True

    def _connect(self, ssid, password, auth_mode=None, timeout=None):
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            self.station.connect(ssid, (auth_mode, password), timeout=int(timeout * 1000))
        else:
            self.station.connect(ssid, password)

    def wait_for_connection(self, timeout=15.0):
        """
        Wait for network to arrive.

        :param timeout:  (Default value = 15.0)

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
        """ """

        # Inquire visible networks.
        log.info("WiFi STA: Scanning for networks")

        # Work around "OSError: Scan operation Failed!" by waiting before `scan`.
        # > I put a time.sleep() of 3sec before wlan.scan(). And the error don't happen.
        # https://forum.pycom.io/topic/5258/firmware-release-v1-20-1/49
        time.sleep(1)

        try:
            stations_available = self.station.scan()
        except Exception as ex:
            log.exc(ex, 'WiFi STA: Scanning for networks failed')
            #if 'Scan operation Failed' in str(ex):
            #    self.station.init()
            return []

        # Collect SSIDs of available stations.
        # (ssid, bssid, channel, RSSI, authmode, hidden)
        try:
            networks_found = frozenset([station.ssid for station in stations_available])
        except AttributeError:
            networks_found = frozenset([station[0] for station in stations_available])

        # Print names/SSIDs of networks found.
        log.info("WiFi STA: Networks available: %s", list(networks_found))

        return stations_available

    def get_ssid(self):
        """ """
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            return self.station.ssid()
        else:
            return self.station.config('essid')

    def get_ip_address(self):
        """ """
        try:
            return self.station.ifconfig()[0]
        except Exception as ex:
            log.exc(ex, 'Unable to get device ip address')

    def get_auth_mode(self, network_name):
        """

        :param network_name: 

        """

        # NVRAM key for storing auth mode per network. Maximum of 15 characters.
        auth_mode_nvs_key = self.auth_mode_nvs_key(network_name.encode())

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

            # log.info('WiFi STA: Neighbourhood is %s', wifi_neighbourhood)

            for station in wifi_neighbourhood:

                # (ssid, bssid, channel, RSSI, authmode, hidden)
                log.debug('Station: %s', station)

                try:
                    ssid = station.ssid
                except AttributeError:
                    ssid = station[0].decode()

                if ssid == network_name:
                    try:
                        auth_mode = station.sec
                    except AttributeError:
                        auth_mode = station[4]
                    break

            if auth_mode is None:
                message = 'WiFi STA: Unable to inquire auth mode for network "{}"'.format(network_name)
                log.warning(message)
                raise WiFiException(message)

            try:
                import pycom

                log.info('WiFi STA: Storing auth mode into NVRAM with key=%s, value=%s', auth_mode_nvs_key, auth_mode)
                try:
                    pycom.nvs_set(auth_mode_nvs_key, auth_mode)
                except Exception as ex:
                    log.exc(ex, 'WiFi STA: Storing auth mode into NVRAM failed')

            except ImportError:
                pass

        return auth_mode

    def auth_mode_nvs_key(self, ssid):
        """Hack to get a short representation of a WiFi SSID in order to
        squeeze it into a NVRAM key with a maximum length of 15 characters.
        
        Fixme: Review this.

        :param ssid: 

        """
        import hashlib
        import ubinascii
        try:
            hashfun = hashlib.sha512
        except AttributeError:
            hashfun = hashlib.sha256
        digest = ubinascii.hexlify(hashfun(ssid).digest()).decode()
        identifier = 'wa.{}'.format(digest[15:27])
        return identifier

    def forget_network(self, network_name):
        """

        :param network_name: 

        """
        log.info('WiFi STA: Forgetting NVRAM data for network "{}"'.format(network_name))
        auth_mode_nvs_key = self.auth_mode_nvs_key(network_name)
        try:
            import pycom
            pycom.nvs_erase(auth_mode_nvs_key)
        except:
            pass

    def print_short_status(self):
        """ """
        log.info('WiFi STA: Connected to "{}" with IP address "{}"'.format(self.get_ssid(), self.get_ip_address()))

    def print_address_status(self):
        """ """

        # Get MAC address.
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            mac_address = self.station.mac()
        else:
            mac_address = self.station.config('mac')

        # Make MAC address human readable.
        mac_address = self.humanize_mac_addresses(mac_address)

        # Get IP address.
        ifconfig = self.station.ifconfig()

        # Display MAC- and IP-address configuration.
        log.info('WiFi STA: Networking address (MAC): %s', mac_address)
        log.info('WiFi STA: Networking address (IP):  %s', ifconfig)

    def humanize_mac_addresses(self, mac):
        """

        :param mac: 

        """
        info = {}
        if hasattr(mac, 'sta_mac'):
            info['sta_mac'] = format_mac_address(binascii.hexlify(mac.sta_mac).decode())
        if hasattr(mac, 'ap_mac'):
            info['ap_mac'] = format_mac_address(binascii.hexlify(mac.ap_mac).decode())
        return info

    def print_metrics(self):
        """ """
        metrics = SystemWiFiMetrics(self.station).read()
        log.info('WiFi STA: Metrics: %s', metrics)


class WiFiException(Exception):
    pass


class SystemWiFiMetrics(AbstractSystemSensor):
    """
    Runtime information from the WiFi bearer.
    """

    def __init__(self, settings, station):
        super().__init__(settings)
        self.station = station

    def read(self):
        """ """

        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
            stats = {}
            #stats['system.wifi.channel'] = self.station.config('channel')

            try:
                stats['system.wifi.rssi'] = self.station.status('rssi')
            except:
                pass

            return stats

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
