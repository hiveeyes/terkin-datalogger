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

from copy import deepcopy
from microWebSrv import MicroWebSrv
from microDNSSrv import MicroDNSSrv

from terkin import logging
from terkin.sensor import BusType
from terkin.sensor.core import serialize_som

log = logging.getLogger(__name__)


# Global reference to webserver object.
webserver = None


class TerkinHttpApi:
    """ """

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
        """ """
        if self.webserver.IsStarted():
            log.info('HTTP server already started')
        else:
            log.info('Starting HTTP server')
            self.webserver.Start(threaded=True)

    def captive(self):
        """Configure transparent captive portal."""
        # To intercept all requests and redirect them.
        self.webserver.SetNotFoundPageUrl("http://hiverize.wifi")
        MicroDNSSrv.Create({'*': '192.168.4.1'})

    # ======
    # System
    # ======

    @MicroWebSrv.route('/status', 'GET')
    @MicroWebSrv.route('/status', 'POST')
    def about(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        return TerkinHttpApi.respond_text(httpResponse, 'OK')

    @MicroWebSrv.route('/about', 'GET')
    def about(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        return TerkinHttpApi.respond_text(httpResponse, TerkinHttpApi.device.application_info.fullname)

    @MicroWebSrv.route('/restart', 'POST')
    def restart(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """

        TerkinHttpApi.respond_text(httpResponse, 'ACK')

        def do_reset():
            """ """
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
        """

        :param httpClient: 
        :param httpResponse: 

        """
        try:
            query_params = httpClient.GetRequestQueryParams()
            format = query_params.get('format', 'json')
            if format == 'json':
                headers = dict(TerkinHttpApi.headers)
                headers.update({'Content-Disposition': 'attachment; filename="settings.json"'})
                return httpResponse.WriteResponseJSONOk(headers=headers, obj=TerkinHttpApi.settings.to_dict())
            elif format == 'python':
                return httpResponse.WriteResponseFileAttachment('/flash/settings.py', 'settings.py', headers=TerkinHttpApi.headers)

        except Exception as ex:
            log.exc(ex, 'GET settings request failed')
            return httpResponse.WriteResponseError(400)

        return httpResponse.WriteResponseNotFound()

    @MicroWebSrv.route('/api/v1/settings', 'PUT')
    def put_settings(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        try:

            # Sanity checks.
            # TODO: Validate the request.
            content_type = httpClient.GetRequestContentType()

            if content_type is None:
                return httpResponse.WriteResponseNotFound()

            if content_type.startswith('application/json'):
                data = httpClient.ReadRequestContentAsJSON()
                TerkinHttpApi.settings.save('settings-user.json', json.dumps(data))
                return TerkinHttpApi.respond_text(httpResponse, 'ACK')

            elif content_type.startswith('text/plain') or content_type.startswith('application/octet-stream'):
                """
                buffer = TerkinHttpApi.read_request(httpClient)
                #print('body:')
                #print(body)
                TerkinHttpApi.settings.save('settings.py', buffer)
                return TerkinHttpApi.respond_text(httpResponse, 'ACK')
                """
                return httpResponse.WriteResponseError(400)

        except Exception as ex:
            log.exc(ex, 'PUT settings request failed')
            return httpResponse.WriteResponseError(500)

        return httpResponse.WriteResponseNotFound()

    @MicroWebSrv.route('/api/v1/setting', 'GET')
    def get_setting(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        try:
            query_data = httpClient.GetRequestQueryParams()
            name = query_data['name']
            log.info('Getting configuration setting "{}"'.format(name))
            value = TerkinHttpApi.settings.get(name)
            log.info('Configuration setting "{}" is "{}"'.format(name, value))
            return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=value)

        except Exception as ex:
            log.exc(ex, 'GET setting request failed')
            return httpResponse.WriteResponseError(500)

    @MicroWebSrv.route('/api/v1/setting', 'PUT')
    def put_setting(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        try:
            query_data = httpClient.GetRequestQueryParams()
            name = query_data['name']
            value = httpClient.ReadRequestContentAsJSON()
            log.info('Setting configuration setting "{}" to "{}"'.format(name, value))
            TerkinHttpApi.settings[name] = value

            value = TerkinHttpApi.settings.get(name)
            log.info('Re-reading configuration setting "{}" as "{}"'.format(name, value))
            return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=value)

        except Exception as ex:
            log.exc(ex, 'PUT setting request failed')
            return httpResponse.WriteResponseError(500)

    @MicroWebSrv.route('/api/v1/reading/last', 'GET')
    def get_settings(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        try:
            return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=TerkinHttpApi.storage.last_reading)

        except Exception as ex:
            log.exc(ex, 'GET last reading request failed')
            return httpResponse.WriteResponseError(500)

        return httpResponse.WriteResponseNotFound()

    def read_request(httpClient):
        """

        :param httpClient: 

        """
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

    @MicroWebSrv.route('/api/v1/peripherals/busses')
    def sensor_index(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        sensor_manager = TerkinHttpApi.device.application_info.application.sensor_manager
        som_info = serialize_som(sensor_manager.busses)
        return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=som_info)

    @MicroWebSrv.route('/api/v1/peripherals/sensors')
    def sensor_index(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        sensor_manager = TerkinHttpApi.device.application_info.application.sensor_manager
        som_info = serialize_som(sensor_manager.sensors)
        return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=som_info)

    @MicroWebSrv.route('/api/v1/sensors/ds18b20')
    def sensor_index_ds18b20(httpClient, httpResponse):
        """

        :param httpClient: 
        :param httpResponse: 

        """
        sensor_manager = TerkinHttpApi.device.application_info.application.sensor_manager
        ds18b20_sensors = []
        #print('sensor_manager.busses:', sensor_manager.busses)

        # Collect information about all DS18B20 sensors connected to all 1-Wire busses.
        for sensor in sensor_manager.sensors:
            if not hasattr(sensor, 'type') or sensor.type != 'DS18B20':
                continue
            bus_info = {
                'bus': sensor.bus.name,
                'pin': sensor.bus.pins.get('data'),
            }
            for address in sensor.bus.get_devices_ascii():
                sensor_info = deepcopy(bus_info)
                sensor_info['address'] = address
                sensor_info['description'] = sensor.get_device_description(address)
                ds18b20_sensors.append(sensor_info)
        return httpResponse.WriteResponseJSONOk(headers=TerkinHttpApi.headers, obj=ds18b20_sensors)

    # ====
    # Demo
    # ====

    @MicroWebSrv.route('/echo/<slot>', 'GET')
    @MicroWebSrv.route('/echo/<slot>', 'POST')
    def echo(httpClient, httpResponse, routeArgs):
        """

        :param httpClient: 
        :param httpResponse: 
        :param routeArgs: 

        """

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
        """

        :param httpResponse: 
        :param text: 

        """
        return httpResponse.WriteResponseOk(headers=TerkinHttpApi.headers, contentType='text/plain',
                                            contentCharset='utf-8', content=text)
