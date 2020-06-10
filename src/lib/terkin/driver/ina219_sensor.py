# -*- coding: utf-8 -*-
# (c) 2019-2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.model import SensorReading
from terkin.sensor import SensorManager, AbstractSensor
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create INA219 sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = INA219Sensor(settings=sensor_info)
    sensor_bus = sensor_manager.get_bus_by_name(sensor_info.get('bus'))
    sensor_object.acquire_bus(sensor_bus)

    return sensor_object


class INA219Sensor(AbstractSensor):
    """
    A generic INA219 sensor component.
    Used by terkin/datalogger to register and read() from this sensor.
    start() & read() are mandatory.
    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.address = self.settings.get('address', 0x40)

    def start(self):
        """
        Setup the INA219 sensor driver.

        :return:
        """

        # Ensure a bus object exists and is ready.
        self.ensure_bus()

        # Initialize the hardware driver.
        try:

            # MicroPython
            if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:
                from ina219 import INA219
                # TODO: Make "shunt_ohms" configurable. The Adafruit breakout board uses a resistor value of 0.1 Ohms.
                self.driver = INA219(shunt_ohms=0.1, i2c=self.bus.adapter, address=self.address)
                # TODO: Optionally invoke "self.driver.configure()".
                self.driver.configure()

            # Adafruit CircuitPython
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:

                # TODO: https://learn.adafruit.com/adafruit-ina219-current-sensor-breakout/python-circuitpython
                # TODO: optional : change configuration to use 32 samples averaging for both bus voltage and shunt voltage

                import adafruit_ina219
                #self.adc_resolution = adafruit_ina219.ADCResolution
                #self.bus_voltage_range = adafruit_ina219.BusVoltageRange
                self.driver = adafruit_ina219.INA219(i2c_bus=self.bus.adapter, addr=self.address)

            else:
                raise NotImplementedError('INA219 driver not implemented on this platform')

            return True

        except Exception as ex:
            log.exc(ex, 'INA219 hardware driver failed')
            return False

    def read(self):
        """
        Read the INA219 sensor.

        :return: SensorReading
        """

        if self.bus is None or self.driver is None:
            return self.SENSOR_NOT_INITIALIZED

        #log.info('Acquire reading from INA219')

        data = {}

        # MicroPython
        if platform_info.vendor in [platform_info.MICROPYTHON.Vanilla, platform_info.MICROPYTHON.Pycom]:

            # Prepare readings.
            values = {
                "bus_voltage": self.driver.voltage(),
                "shunt_voltage": self.driver.shunt_voltage() / 1000.0,
                "current": self.driver.current() / 1000.0,
                "power": self.driver.power() / 1000.0,
            }

            values['psu_voltage'] = values['bus_voltage'] + values['shunt_voltage']

        # Adafruit CircuitPython
        elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:

            values = {

                # Voltage on V- (load side).
                "bus_voltage": self.driver.bus_voltage,

                # Voltage between V+ and V- across the shunt.
                "shunt_voltage": self.driver.shunt_voltage,

                # Current will be acquired in mA, we want A.
                "current": self.driver.current / 1000.0,

                # The power through the load in Watt.
                "power": self.driver.power,

                # Some more values about how the INA219 has been configured.
                # "bus_voltage_range": self.driver.bus_voltage_range,
                # "gain": self.driver.gain,
                # "bus_adc_resolution": self.driver.bus_adc_resolution,
                # "shunt_adc_resolution": self.driver.shunt_adc_resolution,
                # "mode": self.driver.mode,

            }

            values['psu_voltage'] = values['bus_voltage'] + values['shunt_voltage']

            #print(values)
            #print("PSU Voltage:   {:6.3f} V".format(values['bus_voltage'] + values['shunt_voltage']))
            #print("Shunt Voltage: {:9.6f} V".format(values['shunt_voltage']))
            #print("Load Voltage:  {:6.3f} V".format(values['bus_voltage']))
            #print("Current:       {:9.6f} A".format(values['current'] / 1000))

        # Build telemetry payload.
        # TODO: Push this further into the telemetry domain.
        fieldnames = values.keys()
        for name in fieldnames:
            fieldname = self.format_fieldname(name, hex(self.address))
            value = values[name]
            data[fieldname] = value

        if not data:
            log.warning("I2C device {} has no value: {}".format(self.address, data))

        log.debug("I2C data:     {}".format(data))

        reading = SensorReading()
        reading.sensor = self
        reading.data = data

        return reading
