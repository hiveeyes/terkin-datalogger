# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
class SQNS:
    """

    Synopsis::

        sq = SQNS()
        sq.info()
        sq.firmware_info()

        sq.at('showphy')
    """

    def __init__(self):
        from network import LTE
        self.lte = LTE()
        self.at('RRC:setDbgPerm full')

    def at(self, command):
        self.raw('AT!="{}"'.format(command))

    def raw(self, command):
        print('Sending command {}'.format(command))
        print(self.lte.send_at_cmd(command))

    def imei(self):
        self.at('AT+CGSN=1')

    def info(self):
        # https://forum.pycom.io/topic/4022/unable-to-update-gpy-modem-firmware/8
        self.at('AT')
        self.at('ATI')
        self.at('ATZ')

    def firmware_info(self):
        import sqnsupgrade
        sqnsupgrade.info(verbose=True, debug=True)

    def unbrick(self):
        raise NotImplementedError('https://forum.pycom.io/topic/4022/unable-to-update-gpy-modem-firmware/21')


# Activate this to deploy a global instance of this object.
#global sq; sq = SQNS()
