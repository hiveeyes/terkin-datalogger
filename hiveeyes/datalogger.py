# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from . import __version__
from terkin.sensor import MemoryFree
from terkin.datalogger import TerkinDatalogger


class HiveeyesDatalogger(TerkinDatalogger):

    # Application metadata.
    name = 'Hiveeyes MPY data logger'
    version = __version__

    def register_sensors(self):
        super().register_sensors()
        self.device.tlog('Registering Hiveeyes sensors')

        # Add another sensor.
        memfree = MemoryFree()
        self.add_sensor(memfree)
