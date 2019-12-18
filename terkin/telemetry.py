# -*- coding: utf-8 -*-
# (c) 2017-2019 Andreas Motl <andreas@terkin.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import json
from copy import copy
from urllib.parse import urlsplit, urlencode
from terkin import logging
from terkin.util import to_base64, format_exception, get_device_id, urlparse, dformat

log = logging.getLogger(__name__)

#log.setLevel(logging.DEBUG)


class TelemetryManager:
    """Manage a number of telemetry adapters."""

    def __init__(self):
        self.adapters = []
        self.errors_seen = {}
        self.failure_count = {}

    def add_adapter(self, adapter):
        """

        :param adapter: 

        """
        self.adapters.append(adapter)

    def transmit(self, data):
        """

        :param data: 

        """
        outcomes = {}
        for adapter in self.adapters:

            # Dispatch transmission to telemetry adapter.
            outcome = adapter.transmit(data)

            # Todo: Propagate last error message into outcome and obtain here.
            channel = adapter.channel_uri
            outcomes[channel] = outcome

        return outcomes


class TelemetryAdapter:
    """Telemetry node client: Network participant API
    Todo: Implement exponential backoff instead of MAX_FAILURES.


    """

    MAX_FAILURES = 3

    def __init__(self, device=None, target=None):

        self.device = device
        self.target = target

        self.base_uri = self.target['endpoint']
        self.address = self.target.get('address', {})
        self.address['base_uri'] = self.target['endpoint']
        self.data_more = self.target.get('data', {})

        # TODO: Move default value deeper into the framework here?
        self.format = self.target.get('format', TelemetryClient.FORMAT_JSON)
        self.content_encoding = self.target.get('content_encoding')

        self.channel_uri = None
        self.client = None

        self.topology_name = self.target.get('topology')
        self.topology = None

        self.offline = False
        self.failure_count = 0

    def setup(self):
        """ """

        # Resolve designated topology.
        self.topology = self.topology_factory()
        log.info('Telemetry channel topology: %s', self.topology.name)

        # Compute telemetry channel URI.
        self.channel_uri = self.format_uri()
        log.info('Telemetry channel URI: %s', self.channel_uri)

        # Resolve designated telemetry client.
        self.client = self.client_factory()

    def client_factory(self):
        """ """
        client = TelemetryClient(self.channel_uri,
                                 format=self.format,
                                 content_encoding=self.content_encoding,
                                 uri_suffixes=self.topology.uri_suffixes,
                                 settings=self.target.get('settings'),
                                 networking=self.device.networking)
        return client

    def topology_factory(self):
        """ """
        return TelemetryTopologyFactory(name=self.topology_name, adapter=self).create()

    def format_uri(self, **kwargs):
        """

        :param **kwargs: 

        """
        data = copy(self.address)
        data.update(kwargs)
        return self.topology.uri_template.format(**data)

    def transmit(self, data):
        """

        :param data: 

        """

        self.device.watchdog.feed()

        if not self.is_online():
            # Todo: Suppress this message after a while or reduce interval.
            message = 'Adapter is offline, skipping telemetry to {}'.format(self.channel_uri)
            log.warning(message)
            return False

        # Transform into egress telemetry payload
        # using the designated encoder.
        try:
            data = self.transform(data)
        except Exception as ex:
            log.exc(ex, 'Transmission transform for topology "%s" failed', self.topology_name)
            return False

        try:
            outcome = self.client.transmit(data)
            self.reset_errors()
            return outcome

        except Exception as ex:
            self.record_error()
            message = 'Telemetry to {} failed'.format(self.channel_uri)
            if self.offline:
                log.warning(message)
            else:
                log.exc(ex, message)

        return False

    def transform(self, data):
        """

        :param data: 

        """

        # Add predefined "data_more" to telemetry message.
        data.update(self.data_more)

        if not hasattr(self.topology, 'encode'):
            return data

        # Run data through designated encoder, if given.
        encoder = self.topology.encode
        if encoder is None:
            return data
        else:
            data = encoder(data)

        return data

    def is_online(self):
        """ """

        # Short-cut online/offline state.
        return True

        # Todo: Re-enable online/offline state.
        #return self.failure_count < self.MAX_FAILURES

    def record_error(self):
        """ """
        self.failure_count += 1

    def reset_errors(self):
        """ """
        self.failure_count = 0


class CSVTelemetryAdapter(TelemetryAdapter):
    """Telemetry node client: Network participant API.
    
    This will make your node talk CSV.


    """

    def __init__(self, *args, **kwargs):
        TelemetryAdapter.__init__(self, *args, **kwargs)
        self.format = TelemetryClient.FORMAT_CSV

    def transmit(self, data, **kwargs):
        """

        :param data: 
        :param **kwargs: 

        """
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
    TRANSPORT_LORA = 'lora'

    FORMAT_URLENCODED = 'urlencoded'
    FORMAT_JSON = 'json'
    FORMAT_CSV = 'csv'

    FORMAT_CAYENNELPP = 'lpp'

    CONTENT_ENCODING_IDENTITY = 'identity'
    CONTENT_ENCODING_BASE64 = 'base64'

    def __init__(self, uri, format, content_encoding=None, uri_suffixes=None, settings=None, networking=None):

        log.info('Starting Terkin TelemetryClient')
        self.uri = uri

        self.transport = None
        self.handlers = {}

        self.format = format
        self.content_encoding = content_encoding
        self.uri_suffixes = uri_suffixes or {}
        self.settings = settings or {}

        self.networking = networking

        self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        if self.scheme in ['http', 'https']:
            self.transport = TelemetryClient.TRANSPORT_HTTP

        elif self.scheme in ['mqtt']:
            self.transport = TelemetryClient.TRANSPORT_MQTT

        elif self.scheme in ['lora']:
            self.transport = TelemetryClient.TRANSPORT_LORA

    def serialize(self, data):
        """

        :param data: 

        """

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
        """
        :param data: 
        :param uri:  (Default value = None)
        :param serialize:  (Default value = True)
        """

        # Submit telemetry data using HTTP POST request
        # Serialization: x-www-form-urlencoded

        if uri:
            real_uri = uri
        else:
            real_uri = self.uri

        suffix = self.uri_suffixes.get(self.transport, '').format(**self.__dict__)
        real_uri = real_uri + suffix

        handler = self.get_handler(real_uri)


        payload = data
        """
        if "TelemetryTransportLORA" in handler:
            serialize = False
        """

        if serialize:
            payload = self.serialize(data)

        request = {
            'payload': payload,
        }

        return handler.send(request)

    def get_handler(self, uri):
        """

        :param uri: 

        """

        if uri in self.handlers:
            return self.handlers[uri]

        if self.transport == TelemetryClient.TRANSPORT_HTTP:
            handler = TelemetryTransportHTTP(uri, self.format)

        elif self.transport == TelemetryClient.TRANSPORT_MQTT:
            handler = TelemetryTransportMQTT(uri, self.format)

        elif self.transport == TelemetryClient.TRANSPORT_LORA:
            handler = TelemetryTransportLORA(self.networking.lora_manager, self.settings)

        else:
            raise ValueError('Unknown telemetry transport "{}"'.format(self.transport))

        self.handlers[uri] = handler

        return handler


class TelemetryTransportHTTP:
    """ """

    def __init__(self, uri, format):

        self.uri = uri
        self.format = format

        self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        self.content_type = None
        self.resolve_content_type()

    def resolve_content_type(self):
        """ """

        if self.format == TelemetryClient.FORMAT_URLENCODED:
            self.content_type = 'application/x-www-form-urlencoded'

        elif self.format == TelemetryClient.FORMAT_JSON:
            self.content_type = 'application/json'

        elif self.format == TelemetryClient.FORMAT_CSV:
            self.content_type = 'text/csv'

        else:
            raise ValueError('Unknown serialization format for TelemetryTransportHTTP: {}'.format(format))

    def send(self, request_data):
        """Submit telemetry data using HTTP POST request

        :param request_data: 

        """
        log.info('Sending HTTP request to %s', self.uri)
        log.info('Payload:     %s', request_data['payload'])

        import urequests
        response = urequests.post(self.uri, data=request_data['payload'], headers={'Content-Type': self.content_type})
        if response.status_code in [200, 201]:
            return True
        else:
            message = 'HTTP request failed: {} {}\n{}'.format(response.status_code, response.reason, response.content)
            raise TelemetryTransportError(message)


class TelemetryTransportLORA:
    """ """

    lora_socket = None

    def __init__(self, lora_manager, settings):

        self.lora_manager = lora_manager
        self.settings = settings or {}
        self.size = self.settings.get('size', 12)
        self.datarate = self.settings.get('datarate', 0)


    def ensure_lora_socket(self):

        if self.lora_manager.lora_socket is None:
            try:
                self.lora_manager.create_lora_socket()
            except:
                log.error("[LoRa] Could not create LoRa socket")

    def send(self, request_data):
        """
        :param request_data:
        """

        import binascii
        import socket

        self.ensure_lora_socket()

        payload = request_data['payload']
        log.info('[LoRa] Payload (hex) : %s', binascii.hexlify(payload))

        # Send payload
        try:
            log.info('[LoRa] Sending payload ...')
            self.lora_manager.socket.setsockopt(socket.SOL_LORA, socket.SO_DR, self.datarate)
            outcome = self.lora_manager.lora_send(payload)
            log.info('[LoRa] %s bytes sent', outcome)
        except:
            log.exception('[LoRa] Transmission failed')
            return False

        # Receive downlink message
        # rx = self.lora_manager.lora_receive()

        return True


class TelemetryTransportMQTT:
    """MQTT transport for Terkin Telemetry.
    
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

        # v1
        #self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        # v2
        self.target = urlparse(self.uri)

        # Todo: Refactor `get_device_id` somehow better.
        self.client_id = 'terkin.{}'.format(get_device_id())

        # Status flags.
        self.defunct = False
        self.defunctness_reported = False

        # TODO: Start connecting to MQTT broker here already?
        #       Maybe we should defer this to the point where the
        #       first transmission will require it.
        self.ensure_connection()

    def ensure_connection(self):
        """ """
        # Create one MQTTAdapter instance per target host:port.
        if self.target.netloc not in self.connections:
            # TODO: Add more parameters to MQTTAdapter here.
            log.info('Connecting to MQTT broker at {} with username {}. '
                     'client_id={}'.format(self.target.hostname, self.target.username, self.client_id))
            try:
                self.connections[self.target.netloc] = MQTTAdapter(self.client_id,
                                                                   self.target.hostname,
                                                                   username=self.target.username,
                                                                   password=self.target.password)
            except Exception:
                log.warning('Connecting to MQTT broker at {} '
                            'with username {} failed'.format(self.target.hostname, self.target.username))
                # Todo: Re-enable defunctness
                #self.defunct = True

        return self.connections.get(self.target.netloc)

    def get_connection(self):
        """ """
        return self.ensure_connection()

    def send(self, request_data):
        """

        :param request_data: 

        """

        # Evaluate and handle defunctness.
        if self.defunct:
            if not self.defunctness_reported:
                log.error('MQTT transport is defunct, please scan log '
                          'output for previous error messages.')
                self.defunctness_reported = True
            return False

        # Derive MQTT topic string from URI path component.
        topic = self.target.path.lstrip('/')
        if not topic:
            message = 'Empty MQTT topic, please configure MQTT URI with path component or topology with address'
            raise TelemetryTransportError(message)

        # Use payload from request.
        payload = request_data['payload']

        # Reporting.
        log.info('MQTT topic:   %s', topic)
        prettify_log = False
        if prettify_log:
            log.info('MQTT payload:\n\ns', dformat(payload, indent=48))
        else:
            log.info('MQTT payload: %s', payload)

        try:
            connection = self.get_connection()
            connection.publish(topic, payload)

        except TelemetryAdapterError as ex:
            message = 'Protocol adapter not connected: {}'.format(format_exception(ex))
            raise TelemetryTransportError(message)

        return True


class MQTTAdapter:
    """MQTT adapter wrapping the lowlevel MQTT driver.
    Handles a single connection to an MQTT broker.
    
    TODO: Try to make this module reasonably compatible again
          by becoming an adapter for different implementations.
          E.g., what about Paho?


    """

    def __init__(self, client_id, server, port=0, username=None, password=None):

        # TODO: Add more parameters: keepalive=0, ssl=False, ssl_params={}
        self.client_id = client_id
        self.server = server
        self.port = port
        self.username = username
        self.password = password

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
            log.exc(ex, 'Loading MQTT module failed')
            raise

    def ensure_connection(self):
        """Conditionally connect to MQTT broker, if not connected already"""
        if not self.connected:
            self.connect()

    def connect(self):
        """Connect to MQTT broker"""
        try:
            log.info('Connecting to MQTT broker at {} with username {}'.format(self.server, self.username))
            self.connection = self.driver_class(self.client_id, self.server, port=self.port, user=self.username, password=self.password)
            self.connection.DEBUG = True
            self.connection.connect()
            self.connected = True
            log.info('Connecting to MQTT broker at %s succeeded', self.connection.addr)

        except Exception as ex:
            # FIXME: Evaluate exception. "MQTTException: 5" means "Authentication/Authorization failed".
            self.connected = False
            message = 'Connecting to MQTT broker at {} failed: {}'.format(self.server, format_exception(ex))
            log.exc(ex, message)
            raise TelemetryAdapterError(message)

        return self.connected

    def publish(self, topic, payload, retain=False, qos=1):
        """

        :param topic: 
        :param payload: 
        :param retain:  (Default value = False)
        :param qos:  (Default value = 1)

        """

        # Try to (re-)connect to MQTT broker.
        self.ensure_connection()

        if not self.connected:
            message = 'No MQTT connectivity, skipping telemetry'
            log.warning(message)
            raise TelemetryAdapterError(message)

        try:
            # TODO: Make qos level configurable.
            self.connection.publish(topic, payload, retain=retain, qos=qos)

        except OSError as ex:

            message = 'MQTT publishing failed'
            log.exc(ex, message)

            # Signal connection error in order to reconnect on next submission attempt.
            # [Errno 104] ECONNRESET
            # [Errno 113] ECONNABORTED
            try:
                if ex.errno in [104, 113]:
                    self.connected = False
            except AttributeError:
                print('Exception has no "errno" attribute', dir(ex))
                self.connected = False

            message = '{}: {}'.format(message, ex)
            raise TelemetryAdapterError(message)


class TelemetryTopology:
    """Define **how** to communicate using Telemetry."""

    NONE = 'null'
    MQTTKIT = 'mqttkit'
    BEEP_BOB = 'beep-bob'


class TelemetryTopologyFactory:
    """ """

    def __init__(self, name=None, adapter=None):
        self.name = name
        self.adapter = adapter

    def create(self):
        """ """

        if self.name is None or self.name == TelemetryTopology.NONE:
            return IdentityTopology()

        elif self.name == TelemetryTopology.BEEP_BOB:
            return BeepBobTopology(adapter=self.adapter)

        elif self.name == TelemetryTopology.MQTTKIT:
            return MqttKitTopology()

        else:
            raise KeyError('Configured topology "{}" unknown'.format(self.name))


class IdentityTopology:
    """Apply no kind of transformation to telemetry payload
    and provide Base for derivatives of me.


    """
    uri_template = u'{base_uri}'
    uri_suffixes = None

    @property
    def name(self):
        """ """
        return self.__class__.__name__

    def encode(self, data):
        """

        :param data: 

        """
        return data


class BeepBobTopology(IdentityTopology):
    """Define how to communicate with BEEP for BOB.
    
    https://en.wikipedia.org/wiki/Bebop
    
    - https://beep.nl/
    - https://github.com/beepnl/BEEP
    - https://hiverize.org/
    - https://bee-observer.org/


    """
    uri_template = u'{base_uri}'
    uri_suffixes = None

    def __init__(self, adapter=None):
        self.adapter = adapter
        self.settings = self.adapter.device.settings

    def encode(self, data):
        """Encode telemetry data matching the BEEP-BOB interface.
        
        https://gist.github.com/vkuhlen/51f7968266659f37d076bd66d57cdbbd
        https://github.com/Hiverize/FiPy/blob/master/logger/beep.py
        
        Example::
        
            {
                't': 22.66734,
                'h': 52.41612,
                'p': 1002.334,
                'weight': 10.0,
                't_i_1': 23.1875,
                't_i_2': 23.125,
                't_i_3': 23.125,
                't_i_4': 23.1875
            }

        :param data: 

        """

        # Rename all fields to designated BEEP-BOB fields.
        egress_data = {}
        mapping = self.settings.get('sensor_telemetry_map')
        mapping['key'] = 'key'
        for sensor_field, telemetry_field in mapping.items():
            sensor_field = sensor_field.lower()
            if sensor_field in data:
                egress_data[telemetry_field] = data[sensor_field]

        return egress_data


class MqttKitTopology(IdentityTopology):
    """This defines how to communicate in WAN scenarios having a decent
    number of devices rolled out. While this would cover even earth-scale
    addressing scenarios, it will also give you peace of mind in smaller
    setups like multi-project or multi-tenant scenarios. Even for single
    users, the infinite number of available channels is very convenient
    for ad hoc operation scenarios.
    
    - https://getkotori.org/
    - https://getkotori.org/docs/applications/mqttkit.html
    
    - https://hiveeyes.org/
    - https://hiveeyes.org/docs/system/acquisition/


    """
    uri_template = u'{base_uri}/{realm}/{network}/{gateway}/{node}'
    uri_suffixes = {
        TelemetryClient.TRANSPORT_HTTP: '/data',
        TelemetryClient.TRANSPORT_MQTT: '/data.{format}',
    }

class TelemetryTransportError(Exception):
    """ """
    pass


class TelemetryAdapterError(Exception):
    """ """
    pass


def to_cayenne_lpp(data):
    """Serialize plain data dictionary to binary CayenneLPP format.

    :param data: 

    """

    from cayennelpp import LppFrame
    frame = LppFrame()

    channel = {}
    channel['temp']    = 0
    channel['ana_out'] = 0
    channel['hum']     = 0
    channel['press']   = 0
    channel['scale']   = 0

    for key, value in data.items():

        # TODO: Maybe implement different naming conventions.
        name = key.split("_")[0]
        # try:
        #     channel = int(key.split(":")[1])
        # except IndexError:
        #     channel = 0

        if "temperature" in name:
            frame.add_temperature(channel['temp'], value)
            channel['temp'] += 1
        elif "voltage" in name:
            frame.add_analog_output(channel['ana_out'], value)
            channel['ana_out'] += 1
        elif "humidity" in name:
            frame.add_humitidy(channel['hum'], value)
            channel['hum'] += 1
        elif "pressure" in name:
            frame.add_barometer(channel['press'], value)
            channel['press'] += 1
        elif "scale" in name:
            # 2 bytes signed float is easily exceeded when sending values in [g]
            value_kg = float('%.2f' % (value / 1000))
            frame.add_analog_input(channel['scale'], value_kg)
            channel['scale'] += 1
        elif "analog-output" in name:
            frame.add_analog_output(channel, value)
        elif "analog-input" in name:
            frame.add_analog_input(channel, value)
        elif "digital-input" in name:
            frame.add_digital_input(channel, value)
        elif "digital_output" in name:
            frame.add_digital_output(channel, value)
        elif "illuminance" in name:
            frame.add_luminosity(channel, value)
        elif "barometer" in name:
            frame.add_barometer(channel, value)
        elif "presence" in name:
            frame.add_presence(channel, value)
        elif "accelerometer" in name:
            frame.add_accelerometer(channel, value)
        elif "gyrometer" in name:
            frame.add_gyrometer(channel, value)
        elif "gps" in name:
            frame.add_gps(channel, value)

        # TODO: Fork cayenneLPP and implement load cell telemetry.
        # TODO: Add load encoder as ID 122 (3322)
        # http://openmobilealliance.org/wp/OMNA/LwM2M/LwM2MRegistry.html#extlabel
        # http://www.openmobilealliance.org/tech/profiles/lwm2m/3322.xml

        # elif False and "load" in name:
        #     frame.add_load(channel, value)

        # TODO: Map memfree and other baseline sensors appropriately.

        else:
            # TODO: raise Exception here?
            log.info('[CayenneLPP] Sensor type "{}" not found in CayenneLPP'.format(name))

    return frame.bytes()
