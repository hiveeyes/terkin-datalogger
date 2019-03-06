# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import utime
from terkin.device import TerkinDevice


class TerkinDatalogger:

    def __init__(self, settings):
        self.settings = settings
        self.device = None

    def start(self):

        # Main application object.
        self.device = TerkinDevice(name=self.name, version=self.version, settings=self.settings)

        # Disable this if you don't want serial access.
        self.device.enable_serial()

        # Hello world.
        self.device.print_bootscreen()

        # Bootstrap infrastructure.
        self.device.start_networking()
        self.device.start_telemetry()

        # Signal readyness by publishing information about the device.
        # self.device.publish_properties()

        self.register_sensors()

        self._mainloop()

    def register_sensors(self):
        self.device.tlog('Registering Terkin sensors')
        """
        TODO: Add more sensors.
        - Metadata from NetworkManager.station
        - Device stats, see Microhomie
        - >>> import uos; uos.uname()
          (sysname='FiPy', nodename='FiPy', release='1.20.0.rc7', version='v1.9.4-2833cf5 on 2019-02-08', machine='FiPy with ESP32', lorawan='1.0.2', sigfox='1.0.1')
        """
        pass

    def _mainloop(self):
        while True:
            self.loop()

    def loop(self):
        self.device.tlog('Terkin mainloop')

        # Fake measurement.
        data = {"temperature": 42.84, "humidity": 83}

        # Transmit data
        success = self.device.telemetry.transmit(data)
        print('Telemetry success:', success)
        print()

        # Sleep a little bit
        utime.sleep(self.settings.MAINLOOP_INTERVAL)
