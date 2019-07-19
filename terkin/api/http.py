# -*- coding: utf-8 -*-
# (c) 2019 Diren Senger <diren@uni-bremen.de>
# (c) 2019 Vincent Kuhlen <vkuhlen@uni-bremen.de>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
#
# Web server documentation:
# https://github.com/jczic/MicroWebSrv
#
# Original sources:
# https://github.com/hiveeyes/hiveeyes-micropython-firmware/pull/12/files
# https://github.com/Hiverize/FiPy/blob/master/webserver.py
#
import machine
from microWebSrv import MicroWebSrv
from microDNSSrv import MicroDNSSrv

from terkin import logging

log = logging.getLogger(__name__)


class TerkinHttpApi:

    device = None
    settings = None
    headers = None

    def __init__(self, device=None, settings=None):
        log.info('Setting up HTTP API')

        TerkinHttpApi.device = device
        TerkinHttpApi.settings = settings
        TerkinHttpApi.headers = {
            # Work around troubles with CORS in development.
            'Access-Control-Allow-Origin': '*',
            'Application-Name': TerkinHttpApi.device.application.name,
            'Application-Version': TerkinHttpApi.device.application.version,
        }

        # TCP port 80 and files in /flash/www.
        self.webserver = MicroWebSrv()

    def start(self):
        log.info('Starting HTTP server')
        if not self.webserver.IsStarted():
            self.webserver.Start(threaded=True)

    def captive(self):
        """
        Configure transparent captive portal.
        """
        # To intercept all requests and redirect them.
        self.webserver.SetNotFoundPageUrl("http://hiverize.wifi")
        MicroDNSSrv.Create({'*': '192.168.4.1'})

    def respond_text(httpResponse, text):
        httpResponse.WriteResponseOk(headers=TerkinHttpApi.headers, contentType='text/plain', contentCharset='utf-8', content=text)

    @MicroWebSrv.route('/status', 'GET')
    @MicroWebSrv.route('/status', 'POST')
    def about(httpClient, httpResponse):
        TerkinHttpApi.respond_text(httpResponse, 'OK')

    @MicroWebSrv.route('/about', 'GET')
    def about(httpClient, httpResponse):
        TerkinHttpApi.respond_text(httpResponse, TerkinHttpApi.device.application.fullname)

    @MicroWebSrv.route('/restart', 'POST')
    def restart(httpClient, httpResponse):

        TerkinHttpApi.respond_text(httpResponse, 'Restart acknowledged')

        def do_reset():
            log.info('Resetting device')
            machine.reset()

        try:
            import _thread
            _thread.start_new_thread(do_reset, ())
        except:
            do_reset()

    @MicroWebSrv.route('/echo/<slot>', 'GET')
    @MicroWebSrv.route('/echo/<slot>', 'POST')
    def echo(httpClient, httpResponse, routeArgs):

        # Collect information from HTTP request.
        content_type = httpClient.GetRequestContentType()
        query_data = httpClient.GetRequestQueryParams()

        if content_type.startswith('application/json'):
            data = httpClient.ReadRequestContentAsJSON()
        elif content_type.startswith('application/x-www-form-urlencoded'):
            data = httpClient.ReadRequestPostedFormData()

        # Bundle request information.
        payload = {
            'path': routeArgs,
            'content_type': content_type,
            'query': query_data,
            'data': data,
        }
        return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=payload)
