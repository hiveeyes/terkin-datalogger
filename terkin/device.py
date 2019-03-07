import os

import machine
from machine import Timer
from ubinascii import hexlify

from terkin.radio import NetworkManager


class TerkinDevice:

    def __init__(self, name=None, version=None, settings=None):

        self.name = name
        self.version = version
        self.settings = settings

        # Keep track of time since boot.
        self.chrono = Timer.Chrono()
        self.chrono.start()

        self.networking = None

    def start_networking(self):
        self.tlog('Starting networking')

        self.networking = NetworkManager(self.settings.WIFI_NETWORKS)

        # Start WiFi
        self.networking.start_wifi()

        # Wait for network interface to come up.
        self.networking.wait_for_nic()

        # Inform about networking status.
        #self.networking.print_status()

    def start_rtc(self):
        # https://medium.com/@chrismisztur/pycom-uasyncio-installation-94931fc71283
        from machine import RTC
        rtc = RTC()
        rtc.ntp_sync("pool.ntp.org", 360)
        while not rtc.synced():
            time.sleep_ms(50)
        print(rtc.now())

    def start_telemetry(self):
        self.tlog('Starting telemetry')

        # Create a "Node API" telemetry client object
        # TODO: Use values from configuration settings here.
        from terkin.telemetry import TelemetryNode, TelemetryTopologies
        self.telemetry = TelemetryNode(
            # "https://swarm.hiveeyes.org/api",
            # "http://swarm.hiveeyes.org/api-notls",
            "mqtt://swarm.hiveeyes.org",
            address={
                "realm": "hiveeyes",
                "network": "testdrive",
                "gateway": "area-23",
                "node": "node-1",
            },
            topology=TelemetryTopologies.KotoriWanTopology
        )

        # Setup telemetry object
        self.telemetry.setup()

    def enable_serial(self):
        # Disable these two lines if you don't want serial access.
        uart = machine.UART(0, 115200)
        os.dupterm(uart)

    def elapsed(self):
        return self.chrono.read()

    def tlog(self, message):
        now = self.elapsed()
        print('[{}] {}'.format(now, message))

    def print_bootscreen(self):
        """
        Print bootscreen.

        This contains important details about your device
        and the operating system running on it.
        """

        # TODO: Maybe move to TerkinDatalogger.

        # Program name and version.
        title = '{} {}'.format(self.name, self.version.decode())
        print('=' * len(title))
        print(title)
        print('=' * len(title))

        # Machine runtime information.
        print('CPU freq     {} MHz'.format(machine.freq() / 1000000))
        print('Device id    {}'.format(hexlify(machine.unique_id()).decode()))
        print()

        # System memory info (in bytes)
        machine.info()
        print()

        # TODO: Python runtime information.
        """
        >>> import os; os.uname()
        (sysname='FiPy', nodename='FiPy', release='1.20.0.rc7', version='v1.9.4-2833cf5 on 2019-02-08', machine='FiPy with ESP32', lorawan='1.0.2', sigfox='1.0.1')
        """
        runtime_info = os.uname()
        for key in dir(runtime_info):
            if key == '__class__':
                continue
            value = getattr(runtime_info, key)
            print('{:8}: {}'.format(key, value))
        print()

        # TODO: Program authors, contributors and credits.
