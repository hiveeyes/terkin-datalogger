# -*- coding: utf-8 -*-
# (c) 2019-2020 Matthias Mehldau <wetter@hiveeyes.org>
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import ure
import time

from terkin import logging

log = logging.getLogger(__name__)


class SequansLTE:
    """
    Synopsis::

        sq = SequansLTE()
        sq.info()
        sq.firmware_info()

        sq.at('showphy')

    See also:
    - https://git.cicer.de/autonome-zelle/fipy-nbiot-rtd/blob/master/main.py

    """

    def __init__(self, network_manager, settings):
        self.network_manager = network_manager
        self.settings = settings

        from network import LTE
        self.lte = LTE()

        import machine
        self.chrono = machine.Timer.Chrono()
        self.chrono.start()

    def start(self):
        self.lte.init()
        self.attach()
        self.connect()

    def stop(self):
        self.lte.disconnect()
        time.sleep(0.25)

        self.lte.deinit()
        time.sleep(0.25)

    def attach(self):
        log.info('Attaching to LTE')
        self.lte.attach(band=self.settings.get('networking.lte.band'), apn=self.settings.get('networking.lte.apn'))

        self.chrono.reset()
        while True:

            log.info('Signal strength: {}'.format(self.get_signal_strength()))

            if self.lte.isattached():
                break

            if self.chrono.read() > self.settings.get('networking.lte.attach_timeout'):
                raise Exception('Attaching to LTE timed out')

            time.sleep(0.25)

    def connect(self):
        log.info('Connecting to LTE')
        self.lte.connect()

        self.chrono.reset()
        while True:

            if self.lte.isconnected():
                break

            if self.chrono.read() > self.settings.get('networking.lte.connect_timeout'):
                raise Exception('Connecting to LTE timed out')

            time.sleep(0.25)

    def imei(self):
        """
        Return IMEI.
        """
        return self.at('AT+CGSN=1')

    def info(self):
        """
        Get infos from Modem.
        """

        log.info('Signal strength: {}'.format(self.get_signal_strength()))

        self.at('RRC:setDbgPerm full')
        self.at('RRC:showcaps')
        self.at('showver')

        # https://forum.pycom.io/topic/4022/unable-to-update-gpy-modem-firmware/8
        #self.at('AT')
        #self.at('ATI')
        #self.at('ATZ')

    def get_signal_strength(self):
        csq_at = self.lte.send_at_cmd("AT+CSQ")
        csq_line_regex = ure.compile("\n")
        csq_line = csq_line_regex.split(csq_at)
        csq_string_regex = ure.compile(" ")
        csq_string = csq_string_regex.split(csq_line[1])
        csq_comma = csq_string[1]
        csq_num_regex = ure.compile(",")
        csq_num = csq_num_regex.split(csq_comma)
        csq = csq_num[0]
        return csq

    def at(self, command):
        """

        :param command:

        """
        return self.raw('AT!="{}"'.format(command))

    def raw(self, command):
        """

        :param command:

        """
        log.info('Sending: {}'.format(command))
        answer = self.lte.send_at_cmd(command)
        log.info('Answer:  {}'.format(answer))
        return answer

    def firmware_info(self):
        """ """
        import sqnsupgrade
        sqnsupgrade.info(verbose=True, debug=True)

    def unbrick(self):
        """ """
        raise NotImplementedError('https://forum.pycom.io/topic/4022/unable-to-update-gpy-modem-firmware/21')
