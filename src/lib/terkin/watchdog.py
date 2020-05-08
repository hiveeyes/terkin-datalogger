# -*- coding: utf-8 -*-
# (c) 2017-2019 Andreas Motl <andreas@terkin.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging

log = logging.getLogger(__name__)


class Watchdog:
    """The watchdog timer (WDT) is used to restart the system when the
    application crashes and ends up into a non recoverable state. After
    enabling, the application must "feed" the watchdog periodically to
    prevent the timeout from expiring and resetting the system.
    
    https://docs.pycom.io/firmwareapi/pycom/machine/wdt/

    """

    def __init__(self, device=None, settings=None):
        self.device = device
        self.settings = settings
        self.wdt = None
        self.suspended = False

        self.enabled = self.settings.get('main.watchdog.enabled', False)
        self.timeout = self.settings.get('main.watchdog.timeout', 10000)

    def start(self):
        """ 
        Start the watchdog.
        """
        if not self.enabled:
            log.info('Skipping watchdog timer (WDT)')
            return

        watchdog_timeout = self.timeout
        log.info('Starting the watchdog timer (WDT) with timeout {}ms'.format(watchdog_timeout))

        from machine import WDT
        self.wdt = WDT(timeout=watchdog_timeout)

        # Feed Watchdog once.
        self.feed()

    def resume(self):
        """ 
        Resume the watchdog.
        """
        log.info('Resuming watchdog')
        self.suspended = False
        self.reconfigure_minimum_timeout(self.timeout)

    def suspend(self):
        """
        Disabling a started watchdog is not possible, so let's
        just configure it to an ultra large timeout value.
        """

        log.info('Suspending watchdog')
        self.suspended = True
        self.reconfigure_minimum_timeout(999999999)

    def feed(self):
        """ 
        Feed the watchdog.
        """

        if not self.enabled:
            return

        # When in maintenance mode, try to suspend the watchdog.
        #if self.device.status.maintenance and not self.suspended:
        #    self.stop()

        # Always reconfigure to regular timeout when not in maintenance mode.
        #else:
        #    self.suspended = False
        #    self.wdt.init(self.timeout)

        # Feed the watchdog.
        log.debug('Feeding Watchdog')
        self.wdt.feed()

    def reconfigure_minimum_timeout(self, timeout):
        """

        :param timeout: 

        """
        if not self.enabled:
            return
        if timeout >= self.timeout:
            log.info('Reconfiguring watchdog timeout to {} milliseconds'.format(timeout))
            self.wdt.init(timeout)

    def adjust_for_interval(self, interval):
        """

        :param interval: 

        """
        if self.enabled and not self.suspended:
            watchdog_timeout = self.timeout / 1000.0
            if watchdog_timeout - 2 < interval:
                watchdog_timeout_effective = int((interval + 20) * 1000)
                log.warning('Reconfiguring original watchdog timeout {} as it is '
                            'smaller or near the configured sleep time {}'.format(watchdog_timeout, interval))
                self.reconfigure_minimum_timeout(watchdog_timeout_effective)
