# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import time
from machine import enable_irq, disable_irq
from micropython import const

from terkin import logging
from terkin.util import get_platform_info

log = logging.getLogger(__name__)


# Todo: Make this configurable.
#log.setLevel(logging.DEBUG)


class AbstractSystemSensor:

    def __init__(self, settings):
        self.settings = settings
        self.platform_info = get_platform_info()


class SystemMemoryFree(AbstractSystemSensor):
    """Read free memory in bytes."""

    def read(self):
        """ """
        import gc
        value = gc.mem_free()
        return {'system.memfree': value}


class SystemTemperature(AbstractSystemSensor):
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
        """ """
        import machine

        if not hasattr(machine, 'temperature'):
            raise NotImplementedError(
                'Reading the MCU core temperature is not implemented on this platform')

        rawvalue = machine.temperature()

        # Fahrenheit
        # 'system.temperature': 57.77778
        #temperature = (rawvalue - 32) / 1.8

        # Magic
        # 'system.temperature': 41.30435
        value = rawvalue * (44/23) + (-5034/23)

        reading = {'system.temperature': value}
        return reading


class SystemVoltage(AbstractSystemSensor):
    """
    Read the a voltage level by sampling the ADC on a pin connected
    to a voltage divider. As the Pycom expansion board is using
    Pin 16 for battery voltage, this is also used on other boards
    as kind of a convention.
    
    Implementation
    ==============
    Written by Dominik Kapusta <https://github.com/ayoy>. Thanks!
    Improved by Andreas Motl <https://github.com/amotl>.
    
    License
    =======
    The MIT License (MIT)
    
    Copyright (c) 2018 Dominik Kapusta
    
    - https://kapusta.cc/2018/02/02/air-quality-monitor-revisited/
    - https://github.com/ayoy/upython-aq-monitor/blob/lora/lib/adc.py
    
    Documentation
    =============
    - https://docs.pycom.io/firmwareapi/pycom/machine/adc
    - https://docs.pycom.io/tutorials/all/adc
    
    More resources
    ==============
    - https://forum.pycom.io/topic/3776/adc-use-to-measure-battery-level-vin-level
    - https://github.com/hiveeyes/terkin-datalogger/issues/5
    - https://community.hiveeyes.org/t/batterieuberwachung-voltage-divider-und-attenuation-fur-microypthon-firmware/2128


    """

    # How many times to sample the ADC for making a reading.
    adc_sample_count = const(1000)

    def __init__(self, settings):
        """
        Initialized ADC unit.
        """

        super().__init__(settings)

        # ADC Pin to sample from.
        self.pin = None

        # Main resistor value (R1).
        self.resistor_r1 = None

        # Resistor between input pin and ground (R2).
        self.resistor_r2 = None

        # Reference to platform ADC object.
        self.adc = None

        self.setup()

    def setup(self):
        """
        - Configure the appropriate resistor values for computing the voltage.
        - Setup ADC for sampling.
        """

        self.pin = self.settings.get('pin')
        self.resistor_r1 = self.settings.get('resistor_r1')
        self.resistor_r2 = self.settings.get('resistor_r2')
        self.adc_attenuation_db = self.settings.get('adc_attenuation_db', 6.0)
        self.reading_key = self.settings.get('type')

        assert type(self.pin) is str, 'VCC Error: Voltage divider ADC pin invalid'
        assert type(self.resistor_r1) is int, 'VCC Error: Voltage divider resistor value "resistor_r1" invalid'
        assert type(self.resistor_r2) is int, 'VCC Error: Voltage divider resistor value "resistor_r2" invalid'
        assert type(self.adc_attenuation_db) is float, 'VCC Error: ADC attenuation value "adc_attenuation_db" invalid'

        # ADC channel used for sampling the raw value.
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
            from machine import ADC, Pin
            self.adc = ADC(Pin(int(self.pin[1:])))

        elif self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            from machine import ADC
            self.adc = ADC(id=0)

        else:
            raise NotImplementedError('machine.ADC support is not implemented on this platform')

        # Configure attenuation.
        if self.adc_attenuation_db == 0.0:
            self.adc_atten = ADC.ATTN_0DB
        elif self.adc_attenuation_db == 2.5:
            self.adc_atten = ADC.ATTN_2_5DB
        elif self.adc_attenuation_db == 6.0:
            self.adc_atten = ADC.ATTN_6DB
        elif self.adc_attenuation_db == 11.0:
            self.adc_atten = ADC.ATTN_11DB
        else:
            raise ValueError('ADC attenuation value (adc_attenuation_db) not allowed : {}'.format(self.adc_attenuation_db))

    def read(self):
        """Acquire voltage reading by sampling ADC."""
        # Todo: Make attenuation factor configurable.

        # Sample ADC a few times.
        adc_samples = [0.0] * self.adc_sample_count
        adc_mean = 0.0
        i = 0
        log.debug('Reading voltage level on pin {} with voltage divider {}/{}'.format(self.pin, self.resistor_r1, self.resistor_r2))

        # read samples
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
            self.adc.atten(self.adc_atten)
            irq_state = disable_irq()
            while i < self.adc_sample_count:
                adc_samples[i] = self.adc.read()
                adc_mean += adc_samples[i]
                i += 1
            enable_irq(irq_state)

        elif self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            self.adc.init()
            adc_channel = self.adc.channel(attn=self.adc_atten, pin=self.pin)
            irq_state = disable_irq()
            while i < self.adc_sample_count:
                sample = adc_channel()
                adc_samples[i] = sample
                adc_mean += sample
                i += 1
            enable_irq(irq_state)

        else:
            raise NotImplementedError('Reading the ADC is '
                                      'not implemented on this platform')

        adc_mean /= self.adc_sample_count
        adc_variance = 0.0
        for sample in adc_samples:
            adc_variance += (sample - adc_mean) ** 2
        adc_variance /= (self.adc_sample_count - 1)

        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Vanilla:
            # FIXME: Make this work for vanilla ESP32.
            raw_voltage = 0.0
            mean_voltage = 0.0

        elif self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            raw_voltage = adc_channel.value_to_voltage(4095)
            mean_voltage = adc_channel.value_to_voltage(int(adc_mean))

        mean_variance = (adc_variance * 10 ** 6) // (adc_mean ** 2)

        # log.debug("ADC readings. count=%u:\n%s" %(self.adc_sample_count, str(adc_samples)))
        log.debug("SystemVoltage: Mean of ADC readings (0-4095) = %15.13f" % adc_mean)
        log.debug("SystemVoltage: Mean of ADC voltage readings (0-%dmV) = %15.13f" % (raw_voltage, mean_voltage))
        log.debug("SystemVoltage: Variance of ADC readings = %15.13f" % adc_variance)
        log.debug("SystemVoltage: 10**6*Variance/(Mean**2) of ADC readings = %15.13f" % mean_variance)

        resistor_sum = self.resistor_r1 + self.resistor_r2
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            voltage_millivolt = (adc_channel.value_to_voltage(int(adc_mean))) * resistor_sum / self.resistor_r2
        else:
            # FIXME: Make this work for vanilla ESP32.
            voltage_millivolt = 0.0            
        voltage_volt = voltage_millivolt / 1000.0

        # Shut down ADC channel.
        if self.platform_info.vendor == self.platform_info.MICROPYTHON.Pycom:
            adc_channel.deinit()

        log.debug('Voltage level: {}'.format(voltage_volt))

        reading = {self.reading_key: voltage_volt}
        return reading

    def power_off(self):
        """Shut down ADC."""
        log.info('Turning off ADC')
        self.adc.deinit()


class SystemUptime(AbstractSystemSensor):
    """
    Report system uptime.
    https://docs.pycom.io/firmwareapi/micropython/utime.html#utimeticksms
    """

    start_time = time.time()

    def read(self):
        """ """
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
