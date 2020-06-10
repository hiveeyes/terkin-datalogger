# -*- coding: utf-8 -*-
# (c) 2019-2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2019-2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
from terkin import logging
from terkin.util import get_platform_info

log = logging.getLogger(__name__)


class AbstractSensor:
    """Abstract sensor container, containing meta data as readings."""

    SENSOR_NOT_INITIALIZED = object()

    def __init__(self, settings=None):

        self.settings = settings or {}
        self.type = self.settings.get('type')

        self.name = None
        self.family = None
        self.driver = None

        """
        e.g. Multiple onewire sensors are address indexed on a bus.
        """
        self.address = None
        self.bus = None
        self.parameter = {}
        self.pins = {}

    def start(self):
        """ """
        raise NotImplementedError("Must be implemented in sensor driver")

    def set_address(self, address):
        """

        :param address:

        """
        self.address = address

    def register_pin(self, name, pin):
        """

        :param name:
        :param pin:

        """
        self.pins[name] = pin

    def register_parameter(self, name, parameter):
        """

        :param name:
        :param parameter:

        """
        self.parameter[name] = parameter

    def acquire_bus(self, bus):
        """
        Associate sensor object with bus object.
        :param bus:
        """

        # Skip sensor if associated bus is disabled in configuration.
        if bus is None:
            sensor_type = self.settings.get('type', 'unknown').lower()
            sensor_id = self.settings.get('id', self.settings.get('key', sensor_type))
            sensor_bus = self.settings.get('bus')
            log.warning('Bus {} for sensor with id={} and type={} is disabled, '
                        'skipping registration'.format(sensor_bus, sensor_id, sensor_type))

        self.bus = bus

    def ensure_bus(self):
        if self.bus is None or not self.bus.ready:
            raise KeyError('Bus "{}" not ready for "{}"'.format(self.bus.name, self.__class__.__name__))

    def read(self):
        """ """
        raise NotImplementedError()

    def format_fieldname(self, name, address=None, channel=None):
        """

        :param name:
        :param address:

        """
        parts = [name, channel, address, self.bus.name]
        parts = [part for part in parts if part is not None]
        fieldname = '.'.join(parts)
        return fieldname

    def serialize(self):
        """ """
        return dict(serialize_som(self.__dict__, stringify=['bus']))


class AbstractBus:
    """A blueprint for all bus objects."""

    type = None

    def __init__(self, settings):
        """
        convention <type>:<index>
        """
        self.settings = settings
        self.number = self.settings['number']

        # HAL driver adapter.
        self.adapter = None

        # TODO: Publish found 1-Wire devices to MQTT bus and HTTP API.
        self.devices = []
        self.pins = {}

        # Indicate whether the bus driver is ready.
        self.ready = False

        # Indicate whether the bus driver just has been started.
        self.just_started = None

        # Reference to platform information.
        self.platform_info = get_platform_info()

    @property
    def name(self):
        """ """
        return str(self.type) + ":" + str(self.number)

    def register_pin(self, name, pin):
        """

        :param name:
        :param pin:

        """
        self.pins[name] = pin

    def serialize(self):
        """ """
        info = dict(serialize_som(self.__dict__))
        # FIXME: Why is that?
        info.update({'name': self.name, 'type': self.type})
        return info


def serialize_som(thing, stringify=None):
    """Serialize the sensor object model to a representation
    suitable to be served for the device API.

    :param thing:
    :param stringify:  (Default value = None)

    """
    stringify = stringify or []

    if isinstance(thing, list):
        hm = []
        for item in thing:
            hm.append(serialize_som(item))
        return hm

    elif isinstance(thing, dict):
        newthing = {}
        for key, value in thing.items():
            if key in stringify:
                newthing[key] = str(value)
            else:
                newthing[key] = serialize_som(value)
        return newthing

    elif isinstance(thing, (str, int, float, bool, set)) or type(thing) is type(None):
        return thing

    else:
        if hasattr(thing, 'serialize'):
            thing = thing.serialize()
        else:
            thing = str(thing)
        return thing
