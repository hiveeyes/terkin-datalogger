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
# https://github.com/hiveeyes/terkin-datalogger/pull/12/files
# https://github.com/Hiverize/FiPy/blob/master/webserver.py
#
import json

import machine

from copy import deepcopy
from MicroWebSrv2 import MicroWebSrv2, WebRoute, HttpRequest, GET, POST, PUT

from terkin import logging
from terkin.sensor.common import serialize_som

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

        # Webserver settings.
        webserver_port = settings.get('services.api.http.port', 80)

        # Conditionally initialize webserver.
        # TCP port 80 and files in /flash/www.
        # TODO: Make port and htdocs folder configurable.
        global webserver
        if webserver is None:
            log.info('Creating new HTTP server object')
            webserver = MicroWebSrv2()
            webserver.BindAddress = ('0.0.0.0', webserver_port)
        self.webserver = webserver

    def start(self):
        """ """
        if self.webserver.IsRunning:
            log.info('HTTP server already started')
        else:
            log.info('Starting HTTP server')
            self.webserver.SetEmbeddedConfig()
            self.webserver.StartManaged()

    def stop(self):
        self.webserver.Stop()

    def captive(self):
        """
        Configure transparent captive portal.

        Intercept all requests and redirect them to the device.
        """

        # Intercept DNS inquiries.
        from microDNSSrv import MicroDNSSrv
        MicroDNSSrv.Create({'*': '192.168.4.1'})

        # All pages not found will be redirected here.
        self.webserver.NotFoundURL("http://hiverize.wifi")


    # ======
    # System
    # ======

    @WebRoute(GET, '/status')
    @WebRoute(POST, '/status')
    def status(microWebSrv2, request: HttpRequest):
        TerkinHttpApi.respond_text(request, 'OK')

    @WebRoute(GET, '/about')
    def about(microWebSrv2, request: HttpRequest):
        TerkinHttpApi.respond_text(request, TerkinHttpApi.device.application_info.fullname)

    @WebRoute(POST, '/restart')
    def restart(microWebSrv2: MicroWebSrv2, request: HttpRequest):

        TerkinHttpApi.respond_text(request, 'ACK')

        def do_reset():
            """ """
            log.info('Resetting device')
            microWebSrv2.Stop()
            machine.reset()

        try:
            import _thread
            _thread.start_new_thread(do_reset, ())
        except:
            do_reset()

    # ===========
    # Application
    # ===========

    @WebRoute(GET, '/api/v1/settings')
    def get_settings(microWebSrv2, request: HttpRequest):
        try:
            query_params = request.QueryParams
            format = query_params.get('format', 'json')
            if format == 'json':
                headers = dict(TerkinHttpApi.headers)
                headers.update({'Content-Disposition': 'attachment; filename="settings.json"'})
                TerkinHttpApi.respond_json(request, TerkinHttpApi.settings.to_dict())

            elif format == 'python':
                request.Response._headers.update(TerkinHttpApi.headers)
                request.Response.ReturnFile(filename='/flash/settings.py', attachmentName='settings.py')

            else:
                request.Response.ReturnNotFound()

        except Exception as ex:
            log.exc(ex, 'GET settings request failed')
            request.Response.ReturnBadRequest()

    @WebRoute(PUT, '/api/v1/settings')
    def put_settings(microWebSrv2, request: HttpRequest):
        try:

            # Sanity checks.
            # TODO: Validate the request.
            content_type = request.ContentType

            if content_type is None:
                request.Response.ReturnNotFound()

            if content_type.startswith('application/json'):
                data = request.GetPostedJSONObject()
                TerkinHttpApi.settings.save('settings-user.json', json.dumps(data))
                TerkinHttpApi.respond_text(request, 'ACK')

            elif content_type.startswith('text/plain') or content_type.startswith('application/octet-stream'):
                """
                buffer = TerkinHttpApi.read_request(httpClient)
                #print('body:')
                #print(body)
                TerkinHttpApi.settings.save('settings.py', buffer)
                TerkinHttpApi.respond_text(httpResponse, 'ACK')
                """
                request.Response.ReturnBadRequest()

            else:
                request.Response.ReturnNotFound()

        except Exception as ex:
            log.exc(ex, 'PUT settings request failed')
            request.Response.ReturnInternalServerError()

    @WebRoute(GET, '/api/v1/setting')
    def get_setting(microWebSrv2, request: HttpRequest):
        try:
            query_data = request.QueryParams
            name = query_data['name']
            log.info('Getting configuration setting "{}"'.format(name))
            value = TerkinHttpApi.settings.get(name)
            log.info('Configuration setting "{}" is "{}"'.format(name, value))
            TerkinHttpApi.respond_json(request, value)

        except Exception as ex:
            log.exc(ex, 'GET setting request failed')
            request.Response.ReturnInternalServerError()

    @WebRoute(PUT, '/api/v1/setting')
    def put_setting(microWebSrv2, request: HttpRequest):
        try:
            query_data = request.QueryParams
            name = query_data['name']
            value = request.GetPostedJSONObject()
            log.info('Setting configuration setting "{}" to "{}"'.format(name, value))
            TerkinHttpApi.settings[name] = value

            value = TerkinHttpApi.settings.get(name)
            log.info('Re-reading configuration setting "{}" as "{}"'.format(name, value))
            TerkinHttpApi.respond_json(request, value)

        except Exception as ex:
            log.exc(ex, 'PUT setting request failed')
            request.Response.ReturnInternalServerError()

    @WebRoute(GET, '/api/v1/reading/last')
    def get_settings(microWebSrv2, request: HttpRequest):
        try:
            TerkinHttpApi.respond_json(request, TerkinHttpApi.storage.last_reading)
            return

        except Exception as ex:
            log.exc(ex, 'GET last reading request failed')
            request.Response.ReturnInternalServerError()

        request.Response.ReturnNotFound()

    def read_request(request: HttpRequest):
        # Observations show request payloads are capped at ~4308 bytes.
        # https://github.com/jczic/MicroWebSrv/issues/51
        from uio import StringIO
        buffer = StringIO()
        while True:
            try:
                log.info('Reading 4000 bytes from network')
                payload = request.Content
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

    @WebRoute(GET, '/api/v1/peripherals/buses')
    def sensor_index(microWebSrv2, request: HttpRequest):
        sensor_manager = TerkinHttpApi.device.application_info.application.sensor_manager
        som_info = serialize_som(sensor_manager.buses)
        TerkinHttpApi.respond_json(request, som_info)

    @WebRoute(GET, '/api/v1/peripherals/sensors')
    def sensor_index(microWebSrv2, request: HttpRequest):
        sensor_manager = TerkinHttpApi.device.application_info.application.sensor_manager
        som_info = serialize_som(sensor_manager.sensors)
        TerkinHttpApi.respond_json(request, som_info)

    @WebRoute(GET, '/api/v1/sensors/ds18b20')
    def sensor_index_ds18b20(microWebSrv2, request: HttpRequest):
        sensor_manager = TerkinHttpApi.device.application_info.application.sensor_manager
        ds18b20_sensors = []
        #print('sensor_manager.buses:', sensor_manager.buses)

        # Collect information about all DS18B20 sensors connected to all 1-Wire buses.
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

        TerkinHttpApi.respond_json(request, ds18b20_sensors)

    @WebRoute(GET, '/api/v1/sensor/<sensor>')
    def sensor_info(microWebSrv2, request: HttpRequest, routeArgs):
        sensor = routeArgs['sensor']

    # ====
    # Demo
    # ====

    @WebRoute(GET, '/echo/<slot>')
    @WebRoute(POST, '/echo/<slot>')
    def echo(microWebSrv2, request: HttpRequest, routeArgs):

        # Collect information from HTTP request.
        content_type = request.ContentType
        query_data = request.QueryParams

        if content_type.startswith('application/json'):
            data = request.GetPostedJSONObject()

        elif content_type.startswith('application/x-www-form-urlencoded'):
            data = request.GetPostedURLEncodedForm()

        else:
            data = None

        # Bundle request information.
        payload = {
            'path': routeArgs,
            'content_type': content_type,
            'query': query_data,
            'data': data,
        }
        TerkinHttpApi.respond_json(request, payload)

    # =========
    # Utilities
    # =========

    def respond_text(request, text):
        request.Response._headers.update(TerkinHttpApi.headers)
        request.Response._contentType = 'text/plain'
        request.Response._contentCharset = 'utf-8'
        request.Response.ReturnOk(content=text)

    def respond_json(request, data):
        request.Response._headers.update(TerkinHttpApi.headers)
        request.Response.ReturnOkJSON(obj=data)
