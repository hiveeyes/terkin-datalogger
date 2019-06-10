# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from machine import ADC, enable_irq, disable_irq
from micropython import const
from terkin import logging

log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

print('ADC:', dir(ADC))


class SystemMemoryFree:
    """
    Read free memory in bytes.
    """

    def read(self):
        import gc
        value = gc.mem_free()
        return {'system.memfree': value}


class SystemTemperature:
    """
    Read the internal temperature of the MCU.

    - https://docs.micropython.org/en/latest/esp32/quickref.html#general-board-control
    - https://github.com/micropython/micropython-esp32/issues/33
    - https://github.com/micropython/micropython/pull/3933
    - https://github.com/micropython/micropython-esp32/pull/192
    - https://github.com/espressif/esp-idf/issues/146
    - https://forum.pycom.io/topic/2208/new-firmware-release-1-10-2-b1/4
    """

    def read(self):
        import machine

        rawvalue = machine.temperature()

        # Fahrenheit
        # 'system.temperature': 57.77778
        #temperature = (rawvalue - 32) / 1.8

        # Magic
        # 'system.temperature': 41.30435
        value = rawvalue * (44/23) + (-5034/23)

        reading = {'system.temperature': value}
        return reading


class SystemBatteryLevel:
    def read(self):
        pass


class SystemUptime:
    """
    Return system time and uptime in seconds.

    https://docs.pycom.io/firmwareapi/micropython/utime.html#utimeticksms
    """

    start_time = time.time()

    def read(self):
        now = time.time()
        uptime = time.ticks_ms() / 1000.0
        runtime = now - self.start_time
        reading = {
            'system.time': now,
            'system.uptime': uptime,
            'system.runtime': runtime,
        }
        return reading


class SystemHallSensor:
    """
    - https://forum.pycom.io/topic/3537/internal-hall-sensor-question/2
    - https://github.com/micropython/micropython-esp32/pull/211
    - https://www.esp32.com/viewtopic.php?t=481
    """
    pass


class SystemMemoryPeeker:
    """
    ``machine.mem32[]``

    - https://github.com/micropython/micropython-esp32/pull/192#issuecomment-334631994
    """
    pass


class ADC2:
    """
    ::

        adc = machine.ADC(machine.Pin(35))
        adc.atten(machine.ADC.ATTN_11DB)

    - https://github.com/micropython/micropython-esp32/issues/33
    - https://www.esp32.com/viewtopic.php?t=955
    """
    pass
