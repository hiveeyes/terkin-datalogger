# -*- coding: utf-8 -*-
# (c) 2017-2019 Andreas Motl <andreas@terkin.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys

import machine
from machine import Timer
from ubinascii import hexlify

from terkin import logging

log = logging.getLogger(__name__)


class TerkinDevice:

    def __init__(self, name=None, version=None, settings=None):

        self.name = name
        self.version = version
        self.settings = settings

        self.networking = None
        self.telemetry = None

        self.wdt = None
        self.rtc = None

    @property
    def appname(self):
        return '{} {}'.format(self.name, self.version)

    def start_networking(self):
        log.info('Starting networking')

        from terkin.radio import NetworkManager

        self.networking = NetworkManager(self.settings)

        # Initialize LoRa device.
        if self.settings.get('networking.lora.antenna_attached'):
            self.networking.start_lora()
        else:
            log.info("[LoRa] Disabling LoRa interface as no antenna has been attached. "
                     "ATTENTION: Running LoRa without antenna will wreck your device.")

        # Start WiFi.
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

        log.info('Starting the watchdog timer (WDT)')

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
        log.info('RTC: %s', self.rtc.now())

    def run_gc(self):
        """
        Run a garbage collection.
        https://docs.pycom.io/firmwareapi/micropython/gc.html
        """
        import gc
        gc.collect()

    def start_telemetry(self):
        log.info('Starting telemetry')

        from terkin.telemetry import TelemetryManager, TelemetryAdapter, TelemetryTopologies

        self.telemetry = TelemetryManager()

        # Read all designated telemetry targets from configuration settings.
        telemetry_targets = self.settings.get('telemetry.targets')

        # Compute list of all _enabled_ telemetry targets.
        telemetry_candidates = []
        for telemetry_target in telemetry_targets:
            if telemetry_target.get('enabled', False):
                telemetry_candidates.append(telemetry_target)

        # Create adapter objects for each enabled telemetry target.
        for telemetry_target in telemetry_candidates:

            # Shortcut to address information.
            telemetry_address = telemetry_target['address']

            # Create adapter object.
            telemetry_adapter = TelemetryAdapter(
                telemetry_target['endpoint'],
                address={
                    "realm": telemetry_address['realm'],
                    "network": telemetry_address['network'],
                    "gateway": telemetry_address['gateway'],
                    "node": telemetry_address['node'],
                },
                # TODO: Use topology from configuration settings.
                topology=TelemetryTopologies.KotoriWanTopology,
                format=telemetry_target.get('format'),
                content_encoding=telemetry_target.get('encode'),
            )

            # Setup telemetry adapter.
            telemetry_adapter.setup()

            self.telemetry.add_adapter(telemetry_adapter)

    def enable_serial(self):
        # Disable these two lines if you don't want serial access.
        uart = machine.UART(0, 115200)
        os.dupterm(uart)

    def print_bootscreen(self):
        """
        Print bootscreen.

        This contains important details about your device
        and the operating system running on it.
        """

        # TODO: Maybe move to TerkinDatalogger.
        from uio import StringIO
        buffer = StringIO()

        def add(item=''):
            buffer.write(item)
            buffer.write('\n')

        # Program name and version.
        title = '{} {}'.format(self.name, self.version)

        add()
        add('=' * len(title))
        add(title)
        add('=' * len(title))

        # Machine runtime information.
        add('CPU freq     {} MHz'.format(machine.freq() / 1000000))
        add('Device id    {}'.format(hexlify(machine.unique_id()).decode()))
        add()

        # System memory info (in bytes)
        machine.info()
        add()

        # TODO: Python runtime information.
        add('{:8}: {}'.format('Python', sys.version))

        """
        >>> import os; os.uname()
        (sysname='FiPy', nodename='FiPy', release='1.20.0.rc7', version='v1.9.4-2833cf5 on 2019-02-08', machine='FiPy with ESP32', lorawan='1.0.2', sigfox='1.0.1')
        """
        runtime_info = os.uname()
        for key in dir(runtime_info):
            if key == '__class__':
                continue
            value = getattr(runtime_info, key)
            print('value:', value)
            add('{:8}: {}'.format(key, value))
        add()
        add()

        # TODO: Program authors, contributors and credits.

        log.info(buffer.getvalue())
