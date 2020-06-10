# -*- coding: utf-8 -*-
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2019-2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# License: GNU General Public License, Version 3
import time


class SensorReading:
    """
    Object for holding a sensor reading.
    """
    def __init__(self):

        # Reference to the sensor object.
        self.sensor = None

        # Data dictionary of sensor values.
        self.data = None

        # Time when the reading has been taken.
        self.timestamp = time.time()


class DataFrame:
    """
    A collection of sensor readings to be send from device.
    """
    def __init__(self):

        # List of SensorReading objects.
        self.readings = []

        # Data dictionary of all sensor values.
        self.data_in = {}

        # Transformed data dictionary of all sensor values.
        self.data_out = {}

        # Serialized telemetry payload for all sensor values.
        self.payload_out = None
