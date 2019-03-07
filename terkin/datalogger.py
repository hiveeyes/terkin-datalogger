# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import utime
from terkin.device import TerkinDevice


# Maybe refactor to TerkinCore.
class TerkinDatalogger:

    def __init__(self, settings):
        self.settings = settings
        self.device = None
        self.sensors = []

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

        # Signal readyness by publishing information about the device (Microhomie).
        # self.device.publish_properties()

        self.register_sensors()

        self._mainloop()

    def register_sensors(self):
        self.device.tlog('Registering Terkin sensors')
        """
        TODO: Add more sensors.
        - Metadata from NetworkManager.station
        - Device stats, see Microhomie
        """
        pass

    def _mainloop(self):
        # TODO: Refactor by using timers.
        while True:
            self.loop()

    def add_sensor(self, sensor):
        self.sensors.append(sensor)

    def read_sensors(self):
        data = {}
        for sensor in self.sensors:
            sensor_name = sensor.__class__.__name__
            print('Reading sensor "{}"'.format(sensor_name))
            try:
                data.update(sensor.read())
            except Exception as ex:
                print('Reading sensor "{}" failed: {}'.format(sensor_name, ex))
        return data

    def loop(self):
        self.device.tlog('Terkin mainloop')

        # Read sensors.
        data = self.read_sensors()

        # Transmit data.
        success = self.device.telemetry.transmit(data)

        # Evaluate outcome.
        if success:
            self.device.tlog('Telemetry data successfully transmitted')
        else:
            self.device.tlog('Telemetry data transmission failed')

        # Sleep a little bit
        utime.sleep(self.settings.MAINLOOP_INTERVAL)
