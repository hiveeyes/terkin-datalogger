# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import settings
from hiveeyes.datalogger import HiveeyesDatalogger


class HiverizeDatalogger(HiveeyesDatalogger):

    name = 'Hiverize MPY data logger'

    def register_sensors(self):
        super().register_sensors()
        self.device.tlog('Registering Hiverize sensors')

    def loop(self):
        super().loop()
        self.device.tlog('Hiverize mainloop')


def main():
    datalogger = HiverizeDatalogger(settings)
    datalogger.start()


if __name__ == '__main__':
    main()
