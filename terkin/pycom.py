# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import machine
from terkin import logging

log = logging.getLogger(__name__)


class MachineResetCause:
    """
    Machine reset cause and wakeup reason definitions.

    Will produce nice log messages like these.

    - Coming from power on / hard reset::

        {'reset_cause': {'code': 0, 'message': 'PWRON'}, 'wakeup_reason': {'code': 0, 'message': 'PWRON'}}

    - Coming from deep sleep::

        {'reset_cause': {'code': 3, 'message': 'DEEPSLEEP'}, 'wakeup_reason': {'code': 2, 'message': 'RTC'}}

    Works on Pycom MicroPython 1.20.0.rc11, YMMV.
    Pycom MicroPython 1.20.0.rc11 [v1.9.4-0a38f88] on 2019-05-14; FiPy with ESP32, published on 14 May 2019
    """

    reset_causes = {
        machine.PWRON_RESET: 'PWRON',
        machine.HARD_RESET: 'HARD',
        machine.WDT_RESET: 'WDT',
        machine.DEEPSLEEP_RESET: 'DEEPSLEEP',
        machine.SOFT_RESET: 'SOFT',
        machine.BROWN_OUT_RESET: 'BROWN_OUT'
    }

    wakeup_reasons = {
        machine.PIN_WAKE: 'PIN',
        machine.PWRON_WAKE: 'PWRON',
        machine.RTC_WAKE: 'RTC',
        machine.ULP_WAKE: 'ULP',
        # machine.WLAN_WAKE: 'WLAN',
    }

    @classmethod
    def humanize(cls):

        reset_cause_magic = machine.reset_cause()
        wakeup_reason_magic, _ = machine.wake_reason()

        log.debug('Reset cause: %s', reset_cause_magic)
        log.debug('Wakeup reason: %s', wakeup_reason_magic)

        reset_cause_label = cls.reset_causes.get(reset_cause_magic, 'UNKNOWN')
        wakeup_reason_label = cls.wakeup_reasons.get(wakeup_reason_magic, 'UNKNOWN')
        status = {
            'reset_cause': {'code': reset_cause_magic, 'message': reset_cause_label},
            'wakeup_reason': {'code': wakeup_reason_magic, 'message': wakeup_reason_label},
        }
        return status
