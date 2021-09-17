# -*- coding: utf-8 -*-
# (c) 2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2020 Andreas Motl <andreas.motl@terkin.org>
# (c) 2021 Manu Lange <Manu.Lange@plantandfood.co.nz>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.sensor import SensorManager, AbstractSensor
from terkin.util import get_platform_info

log = logging.getLogger(__name__)
platform_info = get_platform_info()


def includeme(sensor_manager: SensorManager, sensor_info):
    """
    Create VE.Direct sensor object.

    :param sensor_manager:
    :param sensor_info:

    :return: sensor_object
    """
    sensor_object = VEDirectSensor(settings=sensor_info)
    return sensor_object


class VEDirectSensor(AbstractSensor):
    """
    About
    =====
    Victron Energy VE.Direct MPPT charge controller sensor component.

    Supported devices
    =================
    - SmartSolar MPPT 100/20
    - SmartSolar MPPT 75/15
    - BlueSolar MPPT 75/15
    - BMV 702 battery monitor

    Resources
    =========
    - https://github.com/karioja/vedirect
    - https://github.com/nznobody/vedirect
    - https://www.victronenergy.com/solar-charge-controllers/smartsolar-mppt-75-10-75-15-100-15-100-20
    - https://www.victronenergy.com/solar-charge-controllers/bluesolar-mppt-150-35
    - https://www.victronenergy.com/battery-monitors/bmv-700
    - https://www.victronenergy.com/live/victronconnect:mppt-solarchargers

    """

    def __init__(self, settings=None):

        super().__init__(settings=settings)

        # Can be overwritten by ``.set_address()``.
        self.device = settings["device"]
        self.timeout = 5
        self.driver = None

    def start(self):
        log.info('Initializing sensor "Victron Energy VE.Direct" on "{}"'.format(self.device))

        # Initialize the hardware driver.
        try:

            # MicroPython
            if platform_info.vendor in [
                platform_info.MICROPYTHON.Vanilla,
                platform_info.MICROPYTHON.Pycom,
            ]:
                try:
                    from vedirect import VEDirect

                    uart = int(self.device)
                    self.driver = VEDirect(serialport=uart, timeout=self.timeout)
                except Exception as e:
                    log.exc(
                        e,
                        "Could not start VEDirect interface on device: {}".format(
                            self.device
                        ),
                    )
                    raise e

            # CPython
            elif platform_info.vendor == platform_info.MICROPYTHON.RaspberryPi:
                from vedirect import VEDirect

                self.driver = VEDirect(serialport=self.device, timeout=self.timeout)

            else:
                raise NotImplementedError(
                    "VEDirect driver not implemented on this platform"
                )

            return True

        except Exception as ex:
            log.exc(ex, "VEDirect hardware driver failed")

    def read(self):
        if not self.driver:
            log.error("VEDirect interface not initialised")
            return
        log.info('Reading sensor "Victron Energy VE.Direct"')

        # Read raw data from sensor.
        data_raw = self.driver.read_data_single()

        # Compute key fragment based on information from data packet.
        if "PID" in data_raw:
            product_id = str(data_raw["PID"])
        else:
            product_id = "unknown-pid"

        # Aggregate measurement values.
        data = {}
        for key, value in data_raw.items():
            key = "vedirect-{}:{}".format(product_id, key)
            data[key] = value

        return data
