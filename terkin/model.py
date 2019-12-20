# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3


class SensorReading:

    def __init__(self):
        self.sensor = None
        self.data = None


class DataFrame:

    def __init__(self):
        self.readings = []
        self.data_in = {}
        self.data_out = {}
        self.payload_out = None
