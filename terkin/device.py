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

    def start_telemetry(self):
        self.tlog('Starting telemetry')

        # Create a "Node API" telemetry client object
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

        # Print startup screen.
        title = '{} {}'.format(self.name, self.version.decode())
        print('=' * len(title))
        print(title)
        print('=' * len(title))
        print('CPU freq     {} MHz'.format(machine.freq() / 1000000))
        print('Device id    {}'.format(hexlify(machine.unique_id()).decode()))
        print()
        machine.info()
        print()
