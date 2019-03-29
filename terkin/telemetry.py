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
from terkin import logging
from urllib.parse import urlsplit, urlencode

log = logging.getLogger(__name__)


class TelemetryManager:

    def __init__(self):
        self.adapters = []

    def add_adapter(self, adapter):
        self.adapters.append(adapter)

    def transmit(self, data):
        outcomes = []
        for adapter in self.adapters:
            try:
                outcome = adapter.transmit(data)
                outcomes.append(outcome)
            except Exception as ex:
                log.exception('Telemetry failed for adapter {}/{}'.format(adapter.base_uri, adapter.address))

        # TODO: Improve by returning dictionary of all outcomes.
        return any(outcomes)


class TelemetryAdapter:
    """
    Telemetry node client: Network participant API
    """

    def __init__(self, base_uri, address=None, uri_template=None, topology=None, format=None, content_encoding=None):

        self.base_uri = base_uri
        self.address = address or {}
        self.address['base_uri'] = base_uri
        self.uri_template = uri_template or '{base_uri}'
        # TODO: Move default value deeper into the framework here?
        self.format = format or TelemetryClient.FORMAT_JSON
        self.content_encoding = content_encoding

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

        log.info('Telemetry channel URI: %s', self.channel_uri)
        self.client = self.client_factory()

    def client_factory(self):
        client = TelemetryClient(self.channel_uri, format=self.format, content_encoding=self.content_encoding, suffixes=self.suffixes)
        return client

    def transmit(self, data):
        return self.client.transmit(data)


class CSVTelemetryAdapter(TelemetryAdapter):
    """
    Telemetry node client: Network participant API.

    This will make your node talk CSV.
    """

    def __init__(self, *args, **kwargs):
        TelemetryAdapter.__init__(self, *args, **kwargs)
        self.format = TelemetryClient.FORMAT_CSV

    def transmit(self, data, **kwargs):
        uri = self.format_uri(**kwargs)
        log.info('Telemetry channel URI for CSV: %s', uri)
        return self.client.transmit(data, uri=uri, serialize=False)


class TelemetryClient:
    """
    A flexible telemetry data client wrapping access to
    different transport adapters and serialization mechanisms.
    """

    TRANSPORT_HTTP = 'http'
    TRANSPORT_MQTT = 'mqtt'

    FORMAT_URLENCODED = 'urlencoded'
    FORMAT_JSON = 'json'
    FORMAT_CSV = 'csv'
    FORMAT_CAYENNELPP = 'lpp'

    CONTENT_ENCODING_IDENTITY = 'identity'
    CONTENT_ENCODING_BASE64 = 'base64'

    def __init__(self, uri, format, content_encoding=None, suffixes=None):

        log.info('Starting Terkin TelemetryClient')
        self.uri = uri

        self.transport = None
        self.handlers = {}

        self.format = format
        self.content_encoding = content_encoding
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
            payload = to_cayenne_lpp(data)

        elif self.format == TelemetryClient.FORMAT_CSV:
            raise NotImplementedError('Serialization format "CSV" not implemented yet')

        else:
            raise ValueError('Unknown serialization format "{}"'.format(self.format))

        # Apply content encoding.
        if self.content_encoding in (None, self.CONTENT_ENCODING_IDENTITY):
            pass

        elif self.content_encoding == self.CONTENT_ENCODING_BASE64:
            payload = to_base64(payload)

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
        log.ingo('HTTP Path:   %s', self.path)
        log.info('Payload:     %s', request_data['payload'])
        self.connection.request("POST", self.path, body=request_data['payload'], headers={'Content-Type': self.content_type})
        response = self.connection.getresponse()
        if response.status == 200:
            return True
        else:
            raise Exception('HTTP request failed: {} {}'.format(response.status, response.reason))


class TelemetryTransportTTN:

    def __init__(self, size=100):
        raise NotImplementedError('Yadda.')

        from cayenneLPP import cayenneLPP

        # TODO: TTN application needs to be setup accordingly to URI in HTTP.
        # self.application = application
        self.size = size

        self.connection = NetworkManager.create_lora_socket()
        self.lpp = cayenneLPP.CayenneLPP(size=100, sock=self.connection)

    def send(self, request_data):
        # TODO: Raise exception if submission failed.
        raise NotImplementedError('Yadda.')


class TelemetryTransportMQTT:
    """
    MQTT transport for Terkin Telemetry.

    This is currently based on the "Pycom MicroPython MQTT module" just called ``mqtt.py``.
    https://github.com/pycom/pycom-libraries/blob/master/lib/mqtt/mqtt.py

    Originally, this was based on the "umqtt.robust" library::

        micropython -m upip install micropython-umqtt.robust micropython-umqtt.simple

    """

    connections = {}

    def __init__(self, uri, format):

        log.info('Telemetry transport: MQTT over TCP over WiFi')

        # Addressing.
        self.uri = uri
        self.format = format
        self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        # TODO: Use device identifier / hardware serial here
        #       to make the MQTT client id more unique.
        self.client_id = "terkin_mqtt_logger"

        # Status flags.
        self.defunct = False
        self.defunctness_reported = False

        # TODO: Start connecting to MQTT broker here already?
        #       Maybe we should defer this to the point where the
        #       first transmission will require it.
        self.start()

    def start(self):
        # Create one MQTTAdapter instance per target host:port.
        if self.netloc not in self.connections:
            # TODO: Add more parameters to MQTTAdapter here.
            try:
                self.connections[self.netloc] = MQTTAdapter(self.client_id, self.netloc)
            except Exception:
                self.defunct = True

    def get_connection(self):
        return self.connections.get(self.netloc)

    def send(self, request_data):

        # Evaluate and handle defunctness.
        if self.defunct:
            if not self.defunctness_reported:
                log.error('MQTT transport is defunct, please scan log '
                          'output for previous error messages.')
                self.defunctness_reported = True
            return False

        # Derive MQTT topic string from URI path component.
        topic = self.path.lstrip('/')

        # Use payload from request.
        payload = request_data['payload']

        # Reporting.
        log.debug('MQTT topic:  ', topic)
        log.debug('MQTT payload:', payload)

        connection = self.get_connection()
        connection.publish(topic, payload)

        return True


class MQTTAdapter:
    """
    MQTT adapter wrapping the lowlevel MQTT driver.
    Handles a single connection to an MQTT broker.

    TODO: Try to make this module reasonably compatible again
          by becoming an adapter for different implementations.
          E.g., what about Paho?
    """

    def __init__(self, client_id, server, port=0):
        self.client_id = client_id
        self.server = server
        self.port = port
        # TODO: Add more parameters: user=None, password=None, keepalive=0, ssl=False, ssl_params={}

        # Transport driver.
        self.driver_class = None
        self.load_driver()

        # Connection instance.
        self.connection = None

        # Status flags.
        self.connected = False

    def load_driver(self):
        """Load MQTT driver module"""

        # TODO: Create abstract MQTT client factory to account for different implementations.
        try:
            from mqtt import MQTTClient
            self.driver_class = MQTTClient

        except Exception as ex:
            log.exception('Loading MQTT module failed')
            raise

    def ensure_connection(self):
        """Conditionally connect to MQTT broker, if not connected already"""
        if not self.connected:
            self.connect()

    def connect(self):
        """Connect to MQTT broker"""
        try:
            log.info('Connecting to MQTT broker')
            self.connection = self.driver_class(self.client_id, self.server, port=self.port)
            self.connection.DEBUG = True
            self.connection.connect()
            log.info('Connecting to MQTT broker at %s succeeded', self.connection.addr)
            self.connected = True

        except Exception as ex:
            log.exception('Connecting to MQTT broker at %s failed'.format(self.server))
            self.connected = False

        return self.connected

    def publish(self, topic, payload, retain=False, qos=1):

        # Try to (re-)connect to MQTT broker.
        self.ensure_connection()

        try:
            # TODO: Make qos level configurable.
            self.connection.publish(topic, payload, retain=retain, qos=qos)
            return True

        except OSError as ex:
            log.exception('MQTT publishing failed')

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


def to_base64(bytes):
    """Encode bytes to base64 encoded string"""
    # TODO: Move to ``util.py``.
    import base64
    return base64.encodebytes(bytes).decode().rstrip()


def to_cayenne_lpp(data):
    """
    Serialize plain data dictionary to binary CayenneLPP format.
    """

    from cayennelpp import LppFrame
    frame = LppFrame()

    for key, value in data.items():

        # TODO: Maybe implement different naming conventions.
        name = key.split("_")[0]
        try:
            channel = int(key.split("_")[1])
        except IndexError:
            channel = 0

        if "temperature" in name:
            frame.add_temperature(channel, value)
        elif "digital-input" in name:
            frame.add_digital_input(channel, value)
        elif "digital_output" in name:
            frame.add_digital_output(channel, value)
        elif "analog-input" in name:
            frame.add_analog_input(channel, value)
        elif "analog-output" in name:
            frame.add_analog_output(channel, value)
        elif "illuminance" in name:
            frame.add_illuminance(channel, value)
        elif "presence" in name:
            frame.add_presence(channel, value)
        elif "humidity" in name:
            frame.add_humidity(channel, value)
        elif "accelerometer" in name:
            frame.add_accelerometer(channel, value)
        elif "barometer" in name:
            frame.add_barometer(channel, value)
        elif "gyrometer" in name:
            frame.add_gyrometer(channel, value)
        elif "gps" in name:
            frame.add_gps(channel, value)

        # TODO: Fork cayenneLPP and implement load cell telemetry.
        # TODO: Add load encoder as ID 122 (3322)
        # http://openmobilealliance.org/wp/OMNA/LwM2M/LwM2MRegistry.html#extlabel
        # http://www.openmobilealliance.org/tech/profiles/lwm2m/3322.xml
        elif False and "load" in name:
            frame.add_load(channel, value)

        # TODO: Map memfree and other baseline sensors appropriately.

        else:
            # TODO: raise Exception here?
            log.info('[CayenneLPP] Sensor type "{}" not found in CayenneLPP'.format(name))

    return frame.bytes()
