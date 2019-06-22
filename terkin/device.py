# -*- coding: utf-8 -*-
# (c) 2017-2019 Andreas Motl <andreas@terkin.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import time

import machine

from terkin import logging
from terkin.pycom import MachineResetCause
from terkin.radio import WiFiException
from terkin.telemetry import TelemetryManager, TelemetryAdapter
from terkin.util import get_device_id

log = logging.getLogger(__name__)


class DeviceStatus:
    """
    Object holding device status information.
    """
    def __init__(self):
        self.networking = False


class TerkinDevice:

    def __init__(self, name=None, version=None, settings=None):

        self.name = name
        self.version = version
        self.settings = settings

        self.device_id = get_device_id()

        self.networking = None
        self.telemetry = None

        self.wdt = None
        self.rtc = None

        self.status = DeviceStatus()

    @property
    def appname(self):
        return '{} {}'.format(self.name, self.version)

    def start_networking(self):
        log.info('Starting networking')

        from terkin.radio import NetworkManager

        self.networking = NetworkManager(self.settings)

        # Start WiFi.
        try:
            self.networking.start_wifi()

            # Wait for network interface to come up.
            self.networking.wait_for_nic()

            self.status.networking = True

        except WiFiException:
            log.error('Network connectivity not available, WiFi failed')
            self.status.networking = False

        # Initialize LoRa device.
        if self.settings.get('networking.lora.antenna_attached'):
            try:
                self.networking.start_lora()
            except:
                log.exception('Unable to start LoRa subsystem')
        else:
            log.info("[LoRa] Disabling LoRa interface as no antenna has been attached. "
                     "ATTENTION: Running LoRa without antenna will wreck your device.")

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

    def configure_rgb_led(self):
        """
        https://docs.pycom.io/tutorials/all/rgbled.html
        """
        import pycom

        # Enable or disable heartbeat.
        rgb_led_heartbeat = self.settings.get('main.rgb_led.heartbeat', True)
        pycom.heartbeat(rgb_led_heartbeat)
        pycom.heartbeat_on_boot(rgb_led_heartbeat)

        # Alternative signalling.
        # Todo: Run this in a separate thread in order not to delay execution of main program flow.
        if not rgb_led_heartbeat:
            for _ in range(2):
                pycom.rgbled(0x001100)
                time.sleep(0.15)
                pycom.rgbled(0x000000)
                time.sleep(0.10)

    def power_off_lte_modem(self):
        """
        We don't use LTE yet.

        https://community.hiveeyes.org/t/lte-modem-des-pycom-fipy-komplett-stilllegen/2161
        https://forum.pycom.io/topic/4877/deepsleep-on-batteries/10
        """
        log.info('Turning off LTE modem')
        try:
            import pycom
            from network import LTE

            # Invoking this will cause `LTE.deinit()` to take around 6(!) seconds.
            #log.info('Enabling LTE modem on boot')
            #pycom.lte_modem_en_on_boot(True)

            log.info('Invoking LTE.deinit()')
            lte = LTE()
            lte.deinit()

            log.info('Turning off LTE modem on boot')
            pycom.lte_modem_en_on_boot(False)

        except:
            log.exception('Shutting down LTE modem failed')

    def power_off_bluetooth(self):
        """
        We don't use Bluetooth yet.
        """
        log.info('Turning off Bluetooth')
        try:
            from network import Bluetooth
            bluetooth = Bluetooth()
            bluetooth.deinit()
        except:
            log.exception('Shutting down Bluetooth failed')

    def start_telemetry(self):
        log.info('Starting telemetry')

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
            try:
                self.create_telemetry_adapter(telemetry_target)
            except:
                log.exception('Creating telemetry adapter failed for target: %s', telemetry_target)

    def create_telemetry_adapter(self, telemetry_target):
        # Create adapter object.
        telemetry_adapter = TelemetryAdapter(
            device=self,
            endpoint=telemetry_target['endpoint'],
            address=telemetry_target.get('address'),
            data=telemetry_target.get('data'),
            topology=telemetry_target.get('topology'),
            format=telemetry_target.get('format'),
            content_encoding=telemetry_target.get('encode'),
        )

        # Setup telemetry adapter.
        telemetry_adapter.setup()

        self.telemetry.add_adapter(telemetry_adapter)

    def enable_serial(self):
        # Disable these two lines if you don't want serial access.
        # The Pycom forum tells us that this is already incorporated into
        # more recent firmwares, so this is probably a thing of the past.
        #uart = machine.UART(0, 115200)
        #os.dupterm(uart)
        pass

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
        add('Device id    {}'.format(self.device_id))
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
            #print('value:', value)
            add('{:8}: {}'.format(key, value))
        add()
        add()

        # Todo: Add program authors, contributors and credits.

        log.info('\n' + buffer.getvalue())

    def power_off(self):
        self.networking.power_off()

    def hibernate(self, interval, deep=False):

        logging.enable_logging()

        if deep:

            # Prepare and invoke deep sleep.
            # https://docs.micropython.org/en/latest/library/machine.html#machine.deepsleep

            log.info('Preparing deep sleep')

            # Set wake up mode.
            self.set_wakeup_mode()

            # Invoke deep sleep.
            log.info('Entering deep sleep for {} seconds'.format(interval))
            machine.deepsleep(int(interval * 1000))

        else:

            log.info('Entering light sleep for {} seconds'.format(interval))

            # Invoke light sleep.
            # https://docs.micropython.org/en/latest/library/machine.html#machine.sleep
            # https://docs.micropython.org/en/latest/library/machine.html#machine.lightsleep
            #
            # As "machine.sleep" seems to be a noop on Pycom MicroPython,
            # we will just use the regular "time.sleep" here.
            # machine.sleep(int(interval * 1000))
            time.sleep(interval)

    def resume(self):
        log.info('Reset cause and wakeup reason: %s', MachineResetCause.humanize())

    def set_wakeup_mode(self):

        # Set wake up parameters.
        """
        The arguments are:

        - pins: a list or tuple containing the GPIO to setup for deepsleep wakeup.

        - mode: selects the way the configured GPIOs can wake up the module.
          The possible values are: machine.WAKEUP_ALL_LOW and machine.WAKEUP_ANY_HIGH.

        - enable_pull: if set to True keeps the pull up or pull down resistors enabled
          during deep sleep. If this variable is set to True, then ULP or capacitive touch
          wakeup cannot be used in combination with GPIO wakeup.

        -- https://community.hiveeyes.org/t/deep-sleep-with-fipy-esp32-on-micropython/1792/12

        This will yield a wake up reason like::

            'wakeup_reason': {'code': 1, 'message': 'PIN'}

        """

        # Todo: ``enable_pull`` or not?

        # From documentation.
        # machine.pin_sleep_wakeup(pins=['P8'], mode=machine.WAKEUP_ALL_LOW, enable_pull=True)

        # Let's try.
        #machine.pin_sleep_wakeup(pins=['P8'], mode=machine.WAKEUP_ALL_LOW, enable_pull=False)
        pass
