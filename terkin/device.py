import os

import machine
import time
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
        self.wdt = None
        self.rtc = None

    def start_networking(self):
        self.tlog('Starting networking')

        self.networking = NetworkManager(self.settings)


        if not self.settings.get('networking.lora.antenna_attached'):
            print("[LoRa] Antenna need to be attached, otherwise device will break")
            return

        # initiating LoRa device
        self.networking.start_lora()

        self.networking.wait_for_lora_join(42)

        time.sleep(2.5)

        # creating socket comes on a upper level
        #if self.networking.lora_joined:
        #    self.networking.create_lora_socket()
        #else:
        #    print("[LoRa] could not initiate network")

        # Start WiFi
        self.networking.start_wifi()

        # Wait for network interface to come up.
        self.networking.wait_for_nic()

        # Inform about networking status.
        #self.networking.print_status()

    def start_wdt(self):
        """
        The WDT is used to restart the system when the application crashes and
        ends up into a non recoverable state. After enabling, the application
        must "feed" the watchdog periodically to prevent it from expiring and
        resetting the system.
        """
        # https://docs.pycom.io/firmwareapi/pycom/machine/wdt.html

        print('INFO: Starting the watchdog timer (WDT)')

        from machine import WDT
        # Enable it with a specified timeout.
        # TODO: Use values from configuration settings here.
        self.wdt = WDT(timeout=5000)
        self.wdt.feed()

    def feed_wdt(self):
        if self.wdt is not None:
            self.wdt.feed()

    def start_rtc(self):
        """
        The RTC is used to keep track of the date and time.
        """
        # https://docs.pycom.io/firmwareapi/pycom/machine/rtc.html
        # https://medium.com/@chrismisztur/pycom-uasyncio-installation-94931fc71283
        import time
        from machine import RTC
        self.rtc = RTC()
        # TODO: Use values from configuration settings here.
        self.rtc.ntp_sync("pool.ntp.org", 360)
        while not self.rtc.synced():
            time.sleep_ms(50)
        print(self.rtc.now())

    def run_gc(self):
        """
        Run a garbage collection.
        https://docs.pycom.io/firmwareapi/micropython/gc.html
        """
        import gc
        gc.collect()

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
