# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3


class DummySensor:

    def read(self):
        # Fake measurement.
        data = {"temperature": 42.84, "humidity": 83}
        return data
