# -*- coding: utf-8 -*-
# (c) 2017-2019 Andreas Motl <andreas@terkin.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
"""
=============================
Setup on MicroPython for Unix
=============================
::

    export MICROPYPATH=`pwd`/dist-packages

    # "json" and "copy" modules
    micropython -m upip install micropython-json micropython-copy

    # HTTP client modules
    micropython -m upip install micropython-http.client micropython-io micropython-time

    # MQTT client modules
    micropython -m upip install micropython-umqtt.robust micropython-umqtt.simple

"""
import json
from copy import copy
from urllib.parse import urlsplit, urlencode


class TelemetryClient:
    """
    A flexible telemetry data client wrapping access to
    different transport adapters and serialization mechanisms.
    """

    TRANSPORT_HTTP = 'http'
    TRANSPORT_MQTT = 'mqtt'

    FORMAT_URLENCODED   = 'urlencoded'
    FORMAT_JSON         = 'json'
    FORMAT_CSV          = 'csv'

    def __init__(self, uri, format, suffixes=None):

        print('Starting Terkin TelemetryClient')
        self.uri = uri

        self.transport = None
        self.handlers = {}

        self.format = format
        self.suffixes = suffixes or {}

        # TODO: Move to TTN Adapter.
        self.ttn_size = 12

        self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        if self.scheme in ['http', 'https']:
            self.transport = TelemetryClient.TRANSPORT_HTTP

        elif self.scheme in ['mqtt']:
            self.transport = TelemetryClient.TRANSPORT_MQTT

    def serialize(self, data):

        # Serialize payload.
        if self.format == TelemetryClient.FORMAT_URLENCODED:
            payload = urlencode(data)

        elif self.format == TelemetryClient.FORMAT_JSON:
            payload = json.dumps(data)

        elif self.format == TelemetryClient.FORMAT_CAYENNELPP:
            payload = data

        elif self.format == TelemetryClient.FORMAT_CSV:
            raise NotImplementedError('Serialization format "CSV" not implemented yet')

        else:
            raise ValueError('Unknown serialization format "{}"'.format(self.format))

        return payload

    def transmit(self, data, uri=None, serialize=True):

        # Submit telemetry data using HTTP POST request
        # Serialization: x-www-form-urlencoded

        if uri:
            real_uri = uri
        else:
            real_uri = self.uri

        suffix = self.suffixes.get(self.transport, '').format(**self.__dict__)
        real_uri = real_uri + suffix

        handler = self.get_handler(real_uri)


        payload = data
        """
        if "TelemetryTransportTTN" in handler:
            serialize = False
        """

        if serialize:
            payload = self.serialize(data)

        request = {
            'payload': payload,
        }

        return handler.send(request)

    def get_handler(self, uri):

        if uri in self.handlers:
            return self.handlers[uri]

        if self.transport == TelemetryClient.TRANSPORT_HTTP:
            handler = TelemetryTransportHTTP(uri, self.format)

        elif self.transport == TelemetryClient.TRANSPORT_MQTT:
            handler = TelemetryTransportMQTT(uri, self.format)

        elif self.transport == TelemetryClient.TRANSPORT_TTN:
            handler = TelemetryTransportTTN(self.ttn_size)

        else:
            raise ValueError('Unknown telemetry transport "{}"'.format(self.transport))

        self.handlers[uri] = handler

        return handler


class TelemetryTransportHTTP:

    def __init__(self, uri, format):

        self.uri = uri
        self.format = format

        self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        self.content_type = None
        self.resolve_content_type()

        # Use "http.client" for unencrypted HTTP connections
        # micropython -m upip install micropython-http.client micropython-io micropython-time
        from http.client import HTTPConnection
        self.connection = HTTPConnection(self.netloc)

        # TODO: Make HTTPS work
        #from http.client import HTTPSConnection
        ##self.connection = HTTPSConnection(self.netloc)

    def resolve_content_type(self):

        if self.format == TelemetryClient.FORMAT_URLENCODED:
            self.content_type = 'application/x-www-form-urlencoded'

        elif self.format == TelemetryClient.FORMAT_JSON:
            self.content_type = 'application/json'

        elif self.format == TelemetryClient.FORMAT_CSV:
            self.content_type = 'text/csv'

        else:
            raise ValueError('Unknown serialization format "{}"'.format(format))

    def send(self, request_data):
        # Submit telemetry data using HTTP POST request
        print('HTTP Path:   ', self.path)
        print('Payload:     ', request_data['payload'])
        self.connection.request("POST", self.path, body=request_data['payload'], headers={'Content-Type': self.content_type})
        response = self.connection.getresponse()
        if response.status == 200:
            return True
        else:
            raise Exception('HTTP request failed: {} {}'.format(response.status, response.reason))


class TelemetryTransportTTN:

    def __init__(self, size=100):

        from cayenneLPP import cayenneLPP

        # TODO: TTN application needs to be setup accordingly to URI in HTTP
        # self.application = application
        self.size = size

        self.connection = NetworkManager.create_lora_socket()
        self.lpp = cayenneLPP.CayenneLPP(size = 100, sock = self.connection)

    def send(self, request_data):

        for k, v in request_data['payload'].items():
            key = k.split("_")[0]
            channel = k.split("_")[1]
            value = v

            # TODO: Fork cayenneLPP add load to 122 (3322)
            # http://openmobilealliance.org/wp/OMNA/LwM2M/LwM2MRegistry.html#extlabel
            # http://www.openmobilealliance.org/tech/profiles/lwm2m/3322.xml

            if "load" in key:
                self.lpp.add_load(value, channel)
            elif "temperatur" in key:
                self.lpp.add_temperature(value, channel)
            elif "digital-input" in key:
                self.lpp.add_digital_input(value, channel)
            elif "digital_output" in key:
                self.lpp.add_digital_output(value, channel)
            elif "analog-input" in key:
                self.lpp.add_analog_input(value, channel)
            elif "analog-output" in key:
                self.lpp.add_analog_output(value, channel)
            elif "illuminance" in key:
                self.lpp.add_illuminance(value, channel)
            elif "presence" in key:
                self.lpp.add_presence(value, channel)
            elif "humidity" in key:
                self.lpp.add_humidity(value, channel)
            elif "accelerometer" in key:
                self.lpp.add_accelerometer(value, channel)
            elif "barometer" in key:
                self.lpp.add_barometer(value, channel)
            elif "gyrometer" in key:
                self.lpp.add_gyrometer(value, channel)
            elif "gps" in key:
                self.lpp.add_gps(value, channel)
            else:
                print("[CayenneLPP] sensor type not found in cayenneLPP: ", key)

        # TODO raise errorcode if not send


class TelemetryTransportMQTT:
    """
    MQTT transport for Terkin Telemetry.

    This is currently based on the "Pycom MicroPython MQTT module" just called ``mqtt.py``.
    https://github.com/pycom/pycom-libraries/blob/master/lib/mqtt/mqtt.py

    Originally, this was based on the "umqtt.robust" library::

        micropython -m upip install micropython-umqtt.robust micropython-umqtt.simple

    TODO: Try to make this module reasonably compatible again
          by becoming an adapter for different implementations.
    """

    def __init__(self, uri, format):

        print('Telemetry transport: MQTT over TCP over WiFi')
        self.uri = uri
        self.format = format
        self.connected = False
        self.defunct = False
        self.defunctness_reported = False

        # TODO: Start connecting to MQTT broker here already?
        #       Maybe we should defer this to the point where the
        #       first transmission will require it.
        self.start()

    def start(self):

        self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        # Load MQTT module.
        # TODO: Create abstract MQTT client factory to account for different implementations.
        try:
            from mqtt import MQTTClient

        except Exception as ex:
            print('ERROR: Loading MQTT module failed. {}'.format(ex))
            self.defunct = True
            return False

        # Connect to MQTT broker.
        # TODO: Try continuous reconnection to MQTT broker.
        try:
            # TODO: Use device identifier / hardware serial here
            #       to make the MQTT client id more unique.
            print('INFO: Connecting to MQTT broker')
            self.connection = MQTTClient("terkin_mqtt_logger", self.netloc)
            self.connection.DEBUG = True
            self.connection.connect()
            print('INFO: Connecting to MQTT broker succeeded')
            self.connected = True

        except Exception as ex:
            print('ERROR: Connecting to MQTT broker failed. {}'.format(ex))
            self.defunct = True
            return False

        return True

    def ensure_connection(self):
        if not self.connected:
            self.start()

    def send(self, request_data):

        # Evaluate and handle defunctness.
        if self.defunct:
            if not self.defunctness_reported:
                print('ERROR: MQTT transport is defunct, please scan log '
                      'output for previous error messages.')
                self.defunctness_reported = True
            return False

        # Try to (re-)connect to MQTT broker.
        self.ensure_connection()

        # Derive MQTT topic string from URI path component.
        topic = self.path.lstrip('/')

        # Reporting.
        print('MQTT topic:  ', topic)
        print('MQTT payload:', request_data['payload'])

        try:
            # TODO: Make qos level configurable.
            self.connection.publish(topic, request_data['payload'], qos=1)
            return True

        except OSError as ex:
            print('ERROR: MQTT publishing failed. {}'.format(ex))

            # Signal connection error in order to reconnect on next submission attempt.
            # [Errno 104] ECONNRESET
            # [Errno 113] ECONNABORTED
            if ex.errno in [104, 113]:
                self.connected = False

            return False


class TelemetryTopologies:
    """
    Define **how** to communicate using Telemetry.
    """

    class KotoriWanTopology:
        """
        This defines how to communicate in WAN scenarios having a decent
        number of devices rolled out. While this would cover even earth-scale
        addressing scenarios, it will also give you peace of mind in smaller
        setups, even in multi-project or multi-tenant environments.

        Just trust us and keep it as a default setting for your journey ;].
        """
        uri_template = u'{base_uri}/{realm}/{network}/{gateway}/{node}'
        suffixes = {
            TelemetryClient.TRANSPORT_HTTP: '/data',
            TelemetryClient.TRANSPORT_MQTT: '/data.{format}',
        }


class TelemetryNode:
    """
    Telemetry node client: Network participant API
    """

    def __init__(self, base_uri, address=None, uri_template=None, topology=None, format=None):

        self.base_uri = base_uri
        self.address = address or {}
        self.address['base_uri'] = base_uri
        self.uri_template = uri_template or '{base_uri}'
        self.format = format or TelemetryClient.FORMAT_JSON

        self.suffixes = None

        if topology:
            self.uri_template = topology.uri_template
            self.suffixes = topology.suffixes

    def format_uri(self, **kwargs):
        data = copy(self.address)
        data.update(kwargs)
        return self.uri_template.format(**data)

    def setup(self):
        self.channel_uri = self.format_uri()

        print('Telemetry channel URI: ', self.channel_uri)
        self.client = self.client_factory()

    def client_factory(self):
        client = TelemetryClient(self.channel_uri, self.format, suffixes=self.suffixes)
        return client

    def transmit(self, data):
        return self.client.transmit(data)


class CSVTelemetryNode(TelemetryNode):
    """
    Telemetry node client: Network participant API.

    This will make your node talk CSV.
    """

    def __init__(self, *args, **kwargs):
        TelemetryNode.__init__(self, *args, **kwargs)
        self.format = TelemetryClient.FORMAT_CSV

    def transmit(self, data, **kwargs):
        uri = self.format_uri(**kwargs)
        print('Telemetry channel URI for CSV: ', uri)
        return self.client.transmit(data, uri=uri, serialize=False)
