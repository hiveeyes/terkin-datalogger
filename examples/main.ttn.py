# -*- coding: utf-8 -*-
#
# Hiveeyes MicroPython Datalogger
# https://github.com/hiveeyes/hiveeyes-micropython-firmware
#
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
import time
import settings
from terkin import logging
from terkin.datalogger import TerkinDatalogger

log = logging.getLogger(__name__)


class ExampleDatalogger(TerkinDatalogger):
    """
    Yet another data logger. This time for MicroPython.
    """

    # Naming things.
    name = 'Example MicroPython Datalogger'

    def loop(self):
        """
        Loop function. Do what I mean.
        """

        # It's your turn.
        log.info('Custom loop')

        # Send dummy payload to TTN over LoRaWAN.
        # TODO: Send real measurement data.
        if self.settings.get('networking.lora.antenna_attached'):
            self.ttn_test()

        # Finally, schedule other system tasks.
        super().loop()

    def read_sensors(self):
        # CayenneLPP example

        # Payload Base64: AWf8sABnAag=
        # Payload Hex:    0167FCB0006701A8
        data = {
            'temperature_0': 42.42,
            'temperature_1': -84.84,
        }
        return data

    def ttn_test(self):
        """
        Send dummy payload to TTN over LoRaWAN, without taking too much Airtime.
        """
        for i in range(1, 39):
            j = i % 10
            if j == 0 or i == 1:
                payload = "ff"
                success = self.device.networking.lora_send(payload)
                if success:
                    print("[LoRa] send:", payload)
            time.sleep(1)


def main():
    """Start the data logger application."""
    datalogger = ExampleDatalogger(settings)
    datalogger.start()


if __name__ == '__main__':
    """Main application entrypoint."""
    main()
