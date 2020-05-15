# -*- coding: utf-8 -*-
# (c) 2017-2019 Andreas Motl <andreas@terkin.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import time

import machine

from umal import ApplicationInfo
from terkin import logging
from terkin.telemetry.core import TelemetryManager, TelemetryAdapter
from terkin.util import get_device_id
from terkin.watchdog import Watchdog

log = logging.getLogger(__name__)


class DeviceStatus:
    """Object holding device status information."""
    def __init__(self):
        self.maintenance = False
        self.networking = False


class TerkinDevice:
    """
    Singleton object for enabling different device-related subsystems
    and providing lowlevel routines for sleep/resume functionality.
    """

    def __init__(self, application_info: ApplicationInfo):

        self.application_info = application_info
        self.platform_info = application_info.platform_info

        self.name = application_info.name
        self.version = application_info.version
        self.settings = application_info.settings

        self.status = DeviceStatus()
        self.watchdog = Watchdog(device=self, settings=self.settings)

        # Conditionally enable terminal on UART0. Default: False.
        #try:
        #    self.terminal = Terminal(self.settings)
        #    self.terminal.start()
        #except Exception as ex:
        #    log.exc(ex, 'Enabling Terminal failed')

        self.device_id = get_device_id()

        self.networking = None
        self.telemetry = None

        self.rtc = None

    def start_networking(self):
        """ 
        Start all configured networking devices.
        """
        log.info('Starting networking')

        from terkin.network import NetworkManager, WiFiException

        self.networking = NetworkManager(device=self, settings=self.settings)

        if self.settings.get('networking.wifi.enabled'):
            # Start WiFi.
            try:
                self.networking.start_wifi()

            except Exception as ex:
                log.exc(ex, 'Starting WiFi networking failed')
                self.status.networking = False
                return

            # Wait for network stack to come up.
            try:
                self.networking.wait_for_ip_stack(timeout=5)
                self.status.networking = True
            except Exception as ex:
                log.exc(ex, 'IP stack not available')
                self.status.networking = False

        else:
            log.info("[WiFi] Interface not enabled in settings.")

        try:
            self.networking.start_services()
        except Exception as ex:
            log.exc(ex, 'Starting network services failed')

        # Initialize LoRa device.
        platform_info = self.application_info.platform_info
        is_pycom_lora = platform_info.device_name in ['LoPy', 'LoPy4', 'FiPy']
        is_dragino = platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi
        if self.settings.get('networking.lora.enabled'):
            if is_pycom_lora or is_dragino:
                if self.settings.get('networking.lora.antenna_attached'):
                    try:
                        self.networking.start_lora()
                        self.status.networking = True
                    except Exception as ex:
                        log.exc(ex, 'Unable to start LoRa subsystem')
                        self.status.networking = False
                else:
                    log.info("[LoRa] Disabling LoRa interface as no antenna has been attached. "
                                 "ATTENTION: Running LoRa without antenna will wreck your device.")
            else:
                log.error("[LoRa] This is not a LoRa capable device.")
        else:
            log.info("[LoRa] Interface not enabled in settings.")

        # Initialize LTE modem.
        if self.settings.get('networking.lte.enabled'):
            try:
                self.networking.start_lte()
                self.status.networking = True
            except Exception as ex:
                log.exc(ex, 'Unable to start LTE modem')
                self.status.networking = False
        else:
            log.info("[LTE]  Interface not enabled in settings.")

        # Initialize GPRS modem.
        if self.settings.get('networking.gprs.enabled'):
            try:
                self.networking.start_gprs()
                self.status.networking = True
            except Exception as ex:
                log.exc(ex, 'Unable to start GPRS modem')
                self.status.networking = False
        else:
            log.info("[GPRS] Interface not enabled in settings.")

        # Inform about networking status.
        #self.networking.print_status()

    def start_rtc(self):
        """
        The RTC is used to keep track of the date and time.
        Syncs RTC with a NTP server.
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
        Curate the garbage collector.
        https://docs.pycom.io/firmwareapi/micropython/gc.html

        For a "quick fix", issue the following periodically.
        https://community.hiveeyes.org/t/timing-things-on-micropython-for-esp32/2329/9

        """
        import gc
        log.info('Start curating the garbage collector')
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
        log.info('Collecting garbage')
        gc.collect()
        #log.info('Curating the garbage collector finished')
        log.info('Curating the garbage collector finished. Free memory: %s', gc.mem_free())

    def configure_rgb_led(self):
        """https://docs.pycom.io/tutorials/all/rgbled.html"""
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            import pycom
            # Enable or disable heartbeat.
            rgb_led_heartbeat = self.settings.get('main.rgb_led.heartbeat', True)
            terkin_blink_pattern = self.settings.get('main.rgb_led.terkin', False)
            if terkin_blink_pattern:
                rgb_led_heartbeat = False
            pycom.heartbeat(rgb_led_heartbeat)
            pycom.heartbeat_on_boot(rgb_led_heartbeat)

    def blink_led(self, color, count=1):
        """

        :param color: 
        :param count:  (Default value = 1)

        """
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            import pycom
            terkin_blink_pattern = self.settings.get('main.rgb_led.terkin', False)
            if terkin_blink_pattern:
                for _ in range(count):
                    pycom.rgbled(color)
                    time.sleep(0.15)
                    pycom.rgbled(0x000000)
                    time.sleep(0.10)

    def start_telemetry(self):
        """ """
        log.info('Starting telemetry')

        self.telemetry = TelemetryManager()

        # Read all designated telemetry targets from configuration settings.
        telemetry_targets = self.settings.get('telemetry.targets', [])

        # Compute list of all _enabled_ telemetry targets.
        telemetry_candidates = []
        for telemetry_target in telemetry_targets:
            if telemetry_target.get('enabled', False):
                telemetry_candidates.append(telemetry_target)

        # Create adapter objects for each enabled telemetry target.
        for telemetry_target in telemetry_candidates:
            try:
                self.create_telemetry_adapter(telemetry_target)
                self.watchdog.feed()

            except Exception as ex:
                log.exc(ex, 'Creating telemetry adapter failed for target: %s', telemetry_target)

    def create_telemetry_adapter(self, telemetry_target):
        """

        :param telemetry_target: 

        """
        # Create adapter object.
        telemetry_adapter = TelemetryAdapter(device=self, target=telemetry_target)

        # Setup telemetry adapter.
        telemetry_adapter.setup()

        self.telemetry.add_adapter(telemetry_adapter)

    def enable_serial(self):
        """ """
        # Disable these two lines if you don't want serial access.
        # The Pycom forum tells us that this is already incorporated into
        # more recent firmwares, so this is probably a thing of the past.
        #uart = machine.UART(0, 115200)
        #os.dupterm(uart)
        pass

    def print_bootscreen(self):
        """Print bootscreen.
        
        This contains important details about your device
        and the operating system running on it.


        """

        if not self.settings.get('main.logging.enabled', False):
            return

        # Todo: Maybe refactor to TerkinDatalogger.
        from uio import StringIO
        buffer = StringIO()

        def add(item=''):
            """

            :param item:  (Default value = '')

            """
            buffer.write(item)
            buffer.write('\n')

        # Program name and version.
        title = '{} {}'.format(self.name, self.version)

        add()
        add('=' * len(title))
        add(title)
        add('=' * len(title))

        # Machine runtime information.
        frequency = machine.freq() / 1000000

        add('Device id    {}'.format(self.device_id))
        add()
        add('CPU freq     {}   MHz'.format(frequency))
        try:
            import pycom
            free_heap = pycom.get_free_heap()
            add('{:13}{:>7} {}'.format('Free heap', free_heap[0] / 1000.0, 'kB'))
            add('{:13}{:>7} {}'.format('Free PSRAM', free_heap[1] / 1000.0, 'kB'))
        except:
            pass
        add()

        # System memory info (in bytes).
        """
        if hasattr(machine, 'info'):
            machine.info()
            add()
        """

        # TODO: Python runtime information.
        add('{:8}: {}'.format('Python', sys.version.replace('\n', '')))
        add('{:8}: {}'.format('platform', sys.platform))

        """
        >>> import os; os.uname()
        (sysname='FiPy', nodename='FiPy', release='1.20.0.rc7', version='v1.9.4-2833cf5 on 2019-02-08', machine='FiPy with ESP32', lorawan='1.0.2', sigfox='1.0.1')
        """
        runtime_info = os.uname()
        #print(dir(runtime_info))
        for key in dir(runtime_info):
            if key.startswith('__') or key.startswith('n_'):
                continue
            value = getattr(runtime_info, key)
            if callable(value):
                continue
            #print('value:', value)
            add('{:8}: {}'.format(key, value))
        add()

        # Todo: Add program authors, contributors and credits.

        log.info('\n' + buffer.getvalue())

    def power_off_lte_modem(self):
        """
        We don't use LTE yet.

        Important
        =========
        Once the LTE radio is initialized, it must be de-initialized
        before going to deepsleep in order to ensure minimum power consumption.
        This is required due to the LTE radio being powered independently and
        allowing use cases which require the system to be taken out from
        deepsleep by an event from the LTE network (data or SMS received for
        instance).

        Note
        ====
        When using the expansion board and the FiPy together, the RTS/CTS
        jumpers MUST be removed as those pins are being used by the LTE radio.
        Keeping those jumpers in place will lead to erratic operation and
        higher current consumption specially while in deepsleep.

        -- https://forum.pycom.io/topic/3090/fipy-current-consumption-analysis/17

        See also
        ========
        - https://community.hiveeyes.org/t/lte-modem-des-pycom-fipy-komplett-stilllegen/2161
        - https://forum.pycom.io/topic/4877/deepsleep-on-batteries/10
        """

        log.info('Turning off LTE modem')
        try:
            import pycom
            from network import LTE

            log.info('Turning off LTE modem on boot')
            pycom.lte_modem_en_on_boot(False)

            # Disables LTE modem completely. This presumably reduces the power
            # consumption to the minimum. Call this before entering deepsleep.
            log.info('Invoking LTE.deinit()')
            lte = LTE()
            lte.deinit(detach=False, reset=True)

        except Exception as ex:
            log.exc(ex, 'Shutting down LTE modem failed')

    def power_off_bluetooth(self):
        """We don't use Bluetooth yet."""

        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
            log.warning("FIXME: Skip touching Bluetooth on vanilla MicroPython "
                        "platforms as we don't use Bluetooth yet")
            return

        log.info('Turning off Bluetooth')
        try:
            from network import Bluetooth
            bluetooth = Bluetooth()
            bluetooth.deinit()
        except Exception as ex:
            log.exc(ex, 'Shutting down Bluetooth failed')

    def hibernate(self, interval, lightsleep=False, deepsleep=False):
        """

        :param interval:
        :param lightsleep:  (Default value = False)
        :param deepsleep:  (Default value = False)

        """

        #logging.enable_logging()

        if deepsleep:

            # Prepare and invoke deep sleep.
            # https://docs.micropython.org/en/latest/library/machine.html#machine.deepsleep

            log.info('Preparing deep sleep')

            # Set wake up mode.
            self.set_wakeup_mode()

            # Invoke deep sleep.
            log.info('Entering deep sleep for {} seconds'.format(interval))
            #self.terminal.stop()
            machine.deepsleep(int(interval * 1000))

        else:

            # Adjust watchdog for interval.
            self.watchdog.adjust_for_interval(interval)

            # Invoke light sleep.
            # https://docs.micropython.org/en/latest/library/machine.html#machine.sleep
            # https://docs.micropython.org/en/latest/library/machine.html#machine.lightsleep
            #
            # As "machine.sleep" seems to be a noop on Pycom MicroPython,
            # we will just use the regular "time.sleep" here.
            # machine.sleep(int(interval * 1000))
            machine.idle()

            if lightsleep:
                log.info('Entering light sleep for {} seconds'.format(interval))
                machine.sleep(int(interval * 1000))

            else:
                # Normal wait.
                log.info('Waiting for {} seconds'.format(interval))
                time.sleep(interval)

    def resume(self):
        """ """
        try:
            from terkin.pycom import MachineResetCause
            log.info('Reset cause and wakeup reason: %s', MachineResetCause().humanize())
        except Exception as ex:
            log.exc(ex, 'Could not determine reset cause and wakeup reason')

    def set_wakeup_mode(self):
        """ """

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
        #log.info('Configuring Pin 4 for wakeup from deep sleep')
        #machine.pin_sleep_wakeup(pins=['P4'], mode=machine.WAKEUP_ALL_LOW, enable_pull=True)
        #machine.pin_sleep_wakeup(pins=['P4'], mode=machine.WAKEUP_ANY_HIGH, enable_pull=True)
        pass


class Terminal:
    """ """

    def __init__(self, settings):
        self.settings = settings
        self.uart = None

    def start(self):
        """Start Terminal on UART0 interface."""
        # Conditionally enable terminal on UART0. Default: False.
        # https://forum.pycom.io/topic/1224/disable-console-to-uart0-to-use-uart0-for-other-purposes
        uart0_enabled = self.settings.get('interfaces.uart0.terminal', False)
        if uart0_enabled:
            from machine import UART
            self.uart = UART(0, 115200)
            #self.uart = UART(0)
            os.dupterm(self.uart)
        else:
            self.shutdown()

    def stop(self):
        """Shut down."""
        log.info('Shutting down Terminal')
        self.shutdown()

    def shutdown(self):
        """Shut down Terminal and UART0 interface."""
        os.dupterm(None)
        self.deinit()

    def deinit(self):
        """Shut down UART0 interface."""
        if self.uart:
            log.info('Shutting down UART0')
            self.uart.deinit()
