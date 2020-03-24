# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.util import get_platform_info

log = logging.getLogger(__name__)


class GPRSManager:
    """ """

    def __init__(self, manager, settings):
        self.manager = manager
        self.settings = settings

        # GPRS settings.
        self.gprs_settings = self.settings.get('networking.gprs')

        # Modem handle.
        self.modem = None

    def start(self):
        """ """
        log.info('[GPRS] Starting GPRS Manager')
        self.start_modem()
        self.connect()

    def start_modem(self):
        """ """

        # Resolve modem driver.
        if self.gprs_settings['driver'] != 'pythings-sim800':
            raise KeyError('Unable to setup unknown modem driver {}'.format(self.gprs_settings['driver']))

        from pythings_sim800 import Modem

        platform_info = get_platform_info()

        # Define two pins for clock and data.
        if platform_info.vendor == platform_info.MICROPYTHON.Vanilla:
            self.modem = Modem(
                MODEM_PWKEY_PIN=int(self.gprs_settings['pin_pwrkey'][1:]),
                MODEM_RST_PIN=int(self.gprs_settings['pin_reset'][1:]),
                MODEM_POWER_ON_PIN=int(self.gprs_settings['pin_power'][1:]),
                MODEM_TX_PIN=int(self.gprs_settings['pin_txd'][1:]),
                MODEM_RX_PIN=int(self.gprs_settings['pin_rxd'][1:]))

        elif platform_info.vendor == platform_info.MICROPYTHON.Pycom:
            self.modem = Modem(
                MODEM_PWKEY_PIN=self.gprs_settings['pin_pwrkey'],
                MODEM_RST_PIN=self.gprs_settings['pin_reset'],
                MODEM_POWER_ON_PIN=self.gprs_settings['pin_power'],
                MODEM_TX_PIN=self.gprs_settings['pin_txd'],
                MODEM_RX_PIN=self.gprs_settings['pin_rxd'])

        else:
            raise NotImplementedError('GPRS modem support is not implemented on this platform')

        # Initialize the modem.
        self.modem.initialize()

    def connect(self):
        # Connect the modem.
        self.modem.connect(apn=self.gprs_settings['apn'])

    def disconnect(self):
        # Disconnect Modem.
        self.modem.disconnect()

    def send_request(self, url, payload, content_type):
        response = self.modem.http_request(url, 'POST', payload, content_type)
        log.info('[GPRS] HTTP response status code: %s', response.status_code)
        log.info('[GPRS] HTTP response content: %s', response.content)
        return response
