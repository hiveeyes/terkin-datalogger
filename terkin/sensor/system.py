# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from machine import ADC, enable_irq, disable_irq
from micropython import const
from terkin import logging

log = logging.getLogger(__name__)

# Todo: Make this configurable.
log.setLevel(logging.DEBUG)


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
    """
    Read the battery level by reading the ADC on a pin connected
    to a voltage divider, which is pin 16 on the expansion board.

    Implementation
    ==============
    Written by Dominik Kapusta <https://github.com/ayoy>. Thanks!

    The MIT License (MIT)

    Copyright (c) 2018 Dominik Kapusta

    - https://kapusta.cc/2018/02/02/air-quality-monitor-revisited/
    - https://github.com/ayoy/upython-aq-monitor/blob/lora/lib/adc.py

    Documentation
    =============
    - https://forum.pycom.io/topic/3776/adc-use-to-measure-battery-level-vin-level
    - https://docs.pycom.io/firmwareapi/pycom/machine/adc
    - https://docs.pycom.io/tutorials/all/adc
    """

    # How many times to sample the ADC for making a reading.
    adc_sample_count = const(1000)

    # Sum of resistor values.
    resistor_sum = 115

    # Resistor between input pin and ground.
    resistor_pin = 56

    def __init__(self):
        """
        Initialized ADC unit.
        """
        self.adc = ADC(id=0)

    def read(self):
        """
        Acquire vbatt reading by sampling ADC.
        """

        # Power on ADC.
        self.adc.init()

        log.debug('Reading battery level')

        # Sample ADC a few times.
        adc_channel = self.adc.channel(attn=ADC.ATTN_6DB, pin='P16')
        adc_samples = [0.0] * self.adc_sample_count
        adc_mean = 0.0
        i = 0
        irq_state = disable_irq()
        while i < self.adc_sample_count:
            sample = adc_channel()
            adc_samples[i] = sample
            adc_mean += sample
            i += 1
        enable_irq(irq_state)

        adc_mean /= self.adc_sample_count
        adc_variance = 0.0
        for sample in adc_samples:
            adc_variance += (sample - adc_mean) ** 2
        adc_variance /= (self.adc_sample_count - 1)

        raw_voltage = adc_channel.value_to_voltage(4095)
        mean_voltage = adc_channel.value_to_voltage(int(adc_mean))
        mean_variance = (adc_variance * 10 ** 6) // (adc_mean ** 2)

        # log.debug("ADC readings. count=%u:\n%s" %(self.adc_sample_count, str(adc_samples)))
        log.debug("SystemBatteryLevel: Mean of ADC readings (0-4095) = %15.13f" % adc_mean)
        log.debug("SystemBatteryLevel: Mean of ADC voltage readings (0-%dmV) = %15.13f" % (raw_voltage, mean_voltage))
        log.debug("SystemBatteryLevel: Variance of ADC readings = %15.13f" % adc_variance)
        log.debug("SystemBatteryLevel: 10**6*Variance/(Mean**2) of ADC readings = %15.13f" % mean_variance)

        voltage_millivolt = (adc_channel.value_to_voltage(int(adc_mean))) * self.resistor_sum / self.resistor_pin
        voltage_volt = voltage_millivolt / 1000.0

        # Shut down ADC channel.
        adc_channel.deinit()

        log.debug('Battery level: {}'.format(voltage_volt))

        reading = {'system.voltage': voltage_volt}
        return reading

    def power_off(self):
        """
        Shut down ADC.
        """
        log.info('Turning off ADC')
        self.adc.deinit()


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
