from . import __version__
from terkin.datalogger import TerkinDatalogger


class HiveeyesDatalogger(TerkinDatalogger):

    # Application metadata.
    name = 'Hiveeyes MPY data logger'
    version = __version__

    def register_sensors(self):
        super().register_sensors()
        self.device.tlog('Registering Hiveeyes sensors')
