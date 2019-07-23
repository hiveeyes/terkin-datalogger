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
import json

import machine
from microWebSrv import MicroWebSrv
from microDNSSrv import MicroDNSSrv

from terkin import logging

log = logging.getLogger(__name__)


# Global reference to webserver object.
webserver = None


class TerkinHttpApi:

    device = None
    settings = None
    storage = None
    headers = None

    def __init__(self, device=None, settings=None, storage=None):

        log.info('Setting up HTTP API')

        TerkinHttpApi.device = device
        TerkinHttpApi.settings = settings
        TerkinHttpApi.storage = storage
        TerkinHttpApi.headers = {
            # Work around troubles with CORS in development.
            'Access-Control-Allow-Origin': '*',

            # Put application name and version into HTTP headers.
            'Application-Name': TerkinHttpApi.device.application_info.name,
            'Application-Version': TerkinHttpApi.device.application_info.version,
        }

        # Conditionally initialize webserver.
        # TCP port 80 and files in /flash/www.
        # TODO: Make port and htdocs folder configurable.
        global webserver
        if webserver is None:
            webserver = MicroWebSrv()
        self.webserver = webserver

    def start(self):
        if self.webserver.IsStarted():
            log.info('HTTP server already started')
        else:
            log.info('Starting HTTP server')
            self.webserver.Start(threaded=True)

    def captive(self):
        """
        Configure transparent captive portal.
        """
        # To intercept all requests and redirect them.
        self.webserver.SetNotFoundPageUrl("http://hiverize.wifi")
        MicroDNSSrv.Create({'*': '192.168.4.1'})

    # ======
    # System
    # ======

    @MicroWebSrv.route('/status', 'GET')
    @MicroWebSrv.route('/status', 'POST')
    def about(httpClient, httpResponse):
        return TerkinHttpApi.respond_text(httpResponse, 'OK')

    @MicroWebSrv.route('/about', 'GET')
    def about(httpClient, httpResponse):
        return TerkinHttpApi.respond_text(httpResponse, TerkinHttpApi.device.application_info.fullname)

    @MicroWebSrv.route('/restart', 'POST')
    def restart(httpClient, httpResponse):

        TerkinHttpApi.respond_text(httpResponse, 'ACK')

        def do_reset():
            log.info('Resetting device')
            machine.reset()

        try:
            import _thread
            _thread.start_new_thread(do_reset, ())
        except:
            do_reset()

    # ===========
    # Application
    # ===========

    @MicroWebSrv.route('/api/v1/settings', 'GET')
    def get_settings(httpClient, httpResponse):
        try:
            query_params = httpClient.GetRequestQueryParams()
            format = query_params.get('format', 'json')
            if format == 'json':
                headers = dict(TerkinHttpApi.headers)
                headers.update({'Content-Disposition': 'attachment; filename="settings.json"'})
                return httpResponse.WriteResponseJSONOk(headers=headers, obj=TerkinHttpApi.settings.to_dict())
            elif format == 'python':
                return httpResponse.WriteResponseFileAttachment('/flash/settings.py', 'settings.py', headers=TerkinHttpApi.headers)

        except:
            log.exception('GET settings request failed')
            return httpResponse.WriteResponseError(400)

        return httpResponse.WriteResponseNotFound()

    @MicroWebSrv.route('/api/v1/settings', 'PUT')
    def put_settings(httpClient, httpResponse):
        try:

            # Sanity checks.
            # TODO: Validate the request.
            content_type = httpClient.GetRequestContentType()

            if content_type is None:
                return httpResponse.WriteResponseNotFound()

            if content_type.startswith('application/json'):
                data = httpClient.ReadRequestContentAsJSON()
                TerkinHttpApi.settings.save('settings.json', json.dumps(data))
                return TerkinHttpApi.respond_text(httpResponse, 'ACK')

            elif content_type.startswith('text/plain') or content_type.startswith('application/octet-stream'):
                buffer = TerkinHttpApi.read_request(httpClient)
                #print('body:')
                #print(body)
                TerkinHttpApi.settings.save('settings.py', buffer)
                return TerkinHttpApi.respond_text(httpResponse, 'ACK')

        except:
            log.exception('PUT settings request failed')
            return httpResponse.WriteResponseError(500)

        return httpResponse.WriteResponseNotFound()

    @MicroWebSrv.route('/api/v1/setting', 'GET')
    def get_setting(httpClient, httpResponse):
        try:
            query_data = httpClient.GetRequestQueryParams()
            name = query_data['name']
            log.info('Getting configuration setting "{}"'.format(name))
            value = TerkinHttpApi.settings.get(name)
            log.info('Configuration setting "{}" is "{}"'.format(name, value))
            return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=value)

        except:
            log.exception('GET setting request failed')
            return httpResponse.WriteResponseError(500)

    @MicroWebSrv.route('/api/v1/setting', 'PUT')
    def put_setting(httpClient, httpResponse):
        try:
            query_data = httpClient.GetRequestQueryParams()
            name = query_data['name']
            value = httpClient.ReadRequestContentAsJSON()
            log.info('Setting configuration setting "{}" to "{}"'.format(name, value))
            TerkinHttpApi.settings[name] = value

            value = TerkinHttpApi.settings.get(name)
            log.info('Re-reading configuration setting "{}" as "{}"'.format(name, value))
            return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=value)

        except:
            log.exception('PUT setting request failed')
            return httpResponse.WriteResponseError(500)

    @MicroWebSrv.route('/api/v1/reading/last', 'GET')
    def get_settings(httpClient, httpResponse):
        try:
            return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=TerkinHttpApi.storage.last_reading)

        except:
            log.exception('GET last reading request failed')
            return httpResponse.WriteResponseError(500)

        return httpResponse.WriteResponseNotFound()

    def read_request(httpClient):
        # Observations show request payloads are capped at ~4308 bytes.
        # https://github.com/jczic/MicroWebSrv/issues/51
        from uio import StringIO
        buffer = StringIO()
        while True:
            try:
                log.info('Reading 4000 bytes from network')
                payload = httpClient.ReadRequestContent(size=4000)
                if not payload:
                    log.info('Reading finished')
                    raise StopIteration()
                log.info('Writing {} bytes to buffer'.format(len(payload)))
                buffer.write(payload)
            except:
                break
        log.info('Rewinding buffer')
        buffer.seek(0)
        return buffer

    @MicroWebSrv.route('/api/v1/sensors/<sensor>')
    def sensors(httpClient, httpResponse, routeArgs):
        sensor = routeArgs['sensor']

    # ====
    # Demo
    # ====

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

    # =========
    # Utilities
    # =========

    def respond_text(httpResponse, text):
        return httpResponse.WriteResponseOk(headers=TerkinHttpApi.headers, contentType='text/plain',
                                            contentCharset='utf-8', content=text)
