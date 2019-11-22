# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019 Matthias Mehldau <wetter@hiveeyes.org>
# License: GNU General Public License, Version 3
import ure
import time


class SQNS:
    """
    Synopsis::
    
        sq = SQNS()
        sq.info()
        sq.firmware_info()
    
        sq.at('showphy')

    See also:
    - https://git.cicer.de/autonome-zelle/fipy-nbiot-rtd/blob/master/main.py

    """

    def __init__(self):
        from network import LTE
        self.lte = LTE()
        self.at('RRC:setDbgPerm full')

    def connect(self):
        self.lte.init()

    def attach(self):
        self.lte.attach(band=8, apn="iot.1nce.net")
        while not self.lte.isattached():  # do we have a timeout?
            time.sleep(1)
            try:
                csq_at = self.lte.send_at_cmd("AT+CSQ")
                csq_line_regex = ure.compile("\n")
                csq_line = csq_line_regex.split(csq_at)
                csq_string_regex = ure.compile(" ")
                csq_string = csq_string_regex.split(csq_line[1])
                csq_comma = csq_string[1]
                csq_num_regex = ure.compile(",")
                csq_num = csq_num_regex.split(csq_comma)
                csq = csq_num[0]
                print("[LTE   ]   ... still attaching ... (CSQ: " + csq + ")")
            except:
                csq = "-999.0"
                print("[LTE   ]   ... no CSQ recevied, let us hope I am still attaching " + csq)

    def at(self, command):
        """

        :param command: 

        """
        self.raw('AT!="{}"'.format(command))

    def raw(self, command):
        """

        :param command: 

        """
        print('Sending command {}'.format(command))
        print(self.lte.send_at_cmd(command))

    def imei(self):
        """ """
        self.at('AT+CGSN=1')

    def info(self):
        """ """
        # https://forum.pycom.io/topic/4022/unable-to-update-gpy-modem-firmware/8
        self.at('AT')
        self.at('ATI')
        self.at('ATZ')

    def firmware_info(self):
        """ """
        import sqnsupgrade
        sqnsupgrade.info(verbose=True, debug=True)

    def unbrick(self):
        """ """
        raise NotImplementedError('https://forum.pycom.io/topic/4022/unable-to-update-gpy-modem-firmware/21')


# Activate this to deploy a global instance of this object.
#global sq; sq = SQNS()
