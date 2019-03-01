# -*- coding: utf-8 -*-
# (c) 2017-2019 Andreas Motl <andreas@terkin.org>

# micropython -m upip install micropython-json micropython-copy
import json

# Problem: "urequests" does not work with SSL, e.g. https://httpbin.org/ip
# micropython -m upip install micropython-urequests
#import urequests

# http.client works
# micropython -m upip install micropython-http.client micropython-io micropython-time

try:
	from urllib import urlsplit, urlencode
	from http.client import HTTPConnection
	from copy import copy
except:
	pass

# micropython -m upip install micropython-umqtt.robust micropython-umqtt.simple
from mqtt import MQTTClient


class TelemetryClient:
    """
    Telemetry data client: Basic API
    """

    TRANSPORT_HTTP = 'http'
    TRANSPORT_MQTT = 'mqtt'

    FORMAT_URLENCODED   = 'urlencoded'
    FORMAT_JSON         = 'json'
    FORMAT_CSV          = 'csv'

    def __init__(self, uri, format, suffixes=None):
        self.uri = uri

        self.transport = None
        self.format = format
        self.suffixes = suffixes or {}
        
        """
        self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        if self.scheme in ['http', 'https']:
            self.transport = TelemetryClient.TRANSPORT_HTTP

        elif self.scheme in ['mqtt']:
        """
        self.transport = TelemetryClient.TRANSPORT_MQTT

    def serialize(self, data):
        payload = None
        if self.format == TelemetryClient.FORMAT_URLENCODED:
            payload = urlencode(data)

        elif self.format == TelemetryClient.FORMAT_JSON:
            payload = json.dumps(data)

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

        if self.transport == TelemetryClient.TRANSPORT_HTTP:
            transport = TelemetryTransportHTTP(real_uri, self.format)

        elif self.transport == TelemetryClient.TRANSPORT_MQTT:
            transport = TelemetryTransportMQTT(real_uri, self.format)

        else:
            raise ValueError('Unknown telemetry transport "{}"'.format(self.transport))

        payload = data
        if serialize:
            payload = self.serialize(data)

        request = {
            'payload': payload,
        }

        return transport.send(request)


class TelemetryTransportHTTP:

    def __init__(self, uri, format):
        self.uri = uri
        self.format = format
        self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)

        # Does not work
        #from http.client import HTTPSConnection
        ##self.connection = HTTPSConnection(self.netloc)

        self.content_type = None
        self.resolve_content_type()

        self.connection = HTTPConnection(self.netloc)

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


class TelemetryTransportMQTT:

    def __init__(self, uri, format):
        self.uri = uri
        self.format = format
        # self.scheme, self.netloc, self.path, self.query, self.fragment = urlsplit(self.uri)
        self.connection = MQTTClient("umqtt_client", "swarm.hiveeyes.org")
        self.connection.DEBUG = True
        self.connection.connect()

    def send(self, request_data):
        topic = "hiveeyes/testdrive/irgendwas/baz/data.json" 
        print('MQTT Topic:  ', topic)
        print('Payload:     ', request_data['payload'])
        self.connection.publish(topic, request_data['payload'])
        return True


class TelemetryTopologies:

    class KotoriWanTopology:

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
        data = self.address
        data.update(kwargs)
        return self.uri_template.format(**data)

    def setup(self):
        self.channel_uri = self.format_uri()

        print('Channel URI: ', self.channel_uri)
        self.client = self.client_factory()

    def client_factory(self):
        client = TelemetryClient(self.channel_uri, self.format, suffixes=self.suffixes)
        return client

    def transmit(self, data):
        return self.client.transmit(data)


class CSVTelemetryNode(TelemetryNode):
    """
    Telemetry node client: Network participant API
    """

    def __init__(self, *args, **kwargs):
        TelemetryNode.__init__(self, *args, **kwargs)
        self.format = TelemetryClient.FORMAT_CSV

    def transmit(self, data, **kwargs):
        uri = self.format_uri(**kwargs)
        print('Channel URI: ', uri)
	return self.client.transmit(data, uri=uri, serialize=False)