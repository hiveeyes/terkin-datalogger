# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import machine

from terkin import logging
from terkin.util import get_platform_info

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

    reset_cause_candidates = [
        'PWRON',
        'HARD',
        'SOFT',
        'WDT',
        'DEEPSLEEP',
        'BROWN_OUT',
    ]

    wakeup_reason_candidates = [
        'PIN',
        'PWRON',
        'RTC',
        'ULP',
        'WLAN',
    ]

    def __init__(self):
        """
        Resolve reset cause and wakeup reason symbols
        and store in dictionary for lookup through
        ``self.humanize()``.
        """

        self.reset_causes = {}
        self.wakeup_reasons = {}

        for name in self.reset_cause_candidates:
            attribute = name + '_RESET'
            symbol = getattr(machine, attribute, None)
            if symbol is not None:
                self.reset_causes[symbol] = name

        for name in self.wakeup_reason_candidates:
            attribute = name + '_WAKE'
            symbol = getattr(machine, attribute, None)
            if symbol is not None:
                self.wakeup_reasons[symbol] = name

    def humanize(self):
        """
        Yield dictionary containing reset cause and wakeup reason
        suitable for human consumption through an appropriate log message.
        """

        platform_info = get_platform_info()

        reset_cause_magic = machine.reset_cause()
        if platform_info.vendor == platform_info.MICROPYTHON.Pycom:
            wakeup_reason_magic, _ = machine.wake_reason()
        else:
            wakeup_reason_magic = machine.wake_reason()

        log.debug('Reset cause: %s', reset_cause_magic)
        log.debug('Wakeup reason: %s', wakeup_reason_magic)

        reset_cause_label = self.reset_causes.get(reset_cause_magic, 'UNKNOWN')
        wakeup_reason_label = self.wakeup_reasons.get(wakeup_reason_magic, 'UNKNOWN')
        status = {
            'reset_cause': {'code': reset_cause_magic, 'message': reset_cause_label},
            'wakeup_reason': {'code': wakeup_reason_magic, 'message': wakeup_reason_label},
        }
        return status
