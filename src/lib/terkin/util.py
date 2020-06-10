# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import uio
import copy
import collections

from umal import PlatformInfo, GenericChronometer


def to_base64(bytes):
    """Encode bytes to base64 encoded string

    :param bytes: 

    """
    # TODO: Move to ``util.py``.
    import base64
    return base64.encodebytes(bytes).decode().rstrip()


def format_exception(ex):
    """

    :param ex: 

    """
    return '{}: {}'.format(ex.__class__.__name__, str(ex))


def get_device_id():
    """ 
    MAC address of device if supported.
    """
    import machine
    from ubinascii import hexlify
    return hexlify(machine.unique_id()).decode()


class URI:
    """ """
    def __str__(self):
        return str(self.__dict__)


def urlparse(url, scheme='', allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>

    :param url: 
    :param scheme:  (Default value = '')
    :param allow_fragments:  (Default value = True)
    :returns: Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes.

    """
    from urllib.parse import uses_params, urlsplit, _splitparams, _coerce_args, ParseResult
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    splitresult = urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = splitresult
    if scheme in uses_params and ';' in url:
        url, params = _splitparams(url)
    else:
        params = ''
    result = ParseResult(scheme, netloc, url, params, query, fragment)

    # FIXME: Appropriately parse netloc into parts using the real ``urlparse``.
    # However, Pycom MicroPython currently lacks the ``rpartition`` method on string objects.

    uri = URI()
    for fieldname in ['scheme', 'netloc', 'path', 'params', 'query', 'fragment']:
        key = fieldname
        value = getattr(result, fieldname)
        #print(key, value)
        setattr(uri, key, value)

    setattr(uri, 'hostname', uri.netloc)
    setattr(uri, 'username', None)
    setattr(uri, 'password', None)

    #print('URI-1:', uri)

    # Manually parse credentials from netloc.
    # Fixme: Improve urlparse to do the same.
    if '@' in uri.netloc:
        credentials, hostname = uri.netloc.split('@')
        username, password = credentials.split(':')

        setattr(uri, 'hostname', hostname)
        setattr(uri, 'username', username)
        setattr(uri, 'password', password)

    #print('URI-2:', uri)

    return uri


def str_grouper(n, iterable):
    """

    :param n: 
    :param iterable: 

    """
    # https://stackoverflow.com/questions/11006702/elegant-format-for-a-mac-address-in-python-3-2/11006779#11006779
    args = [iter(iterable)] * n
    for part in zip(*args):  # itertools.izip in 2.x for efficiency.
        yield "".join(part)


def format_mac_address(mac_address):
    """

    :param mac_address: 

    """
    return ":".join(str_grouper(2, mac_address)).lower()


def dformat(data, indent=0):
    """

    :param data: 
    :param indent:  (Default value = 0)

    """
    padding = ' ' * indent
    from uio import StringIO
    buffer = StringIO()
    for key in sorted(data.keys()):
        value = data[key]
        buffer.write('{}{}: {}\n'.format(padding, key, value))
    return buffer.getvalue()


def ddformat(data, indent=0):
    """

    :param data: 
    :param indent:  (Default value = 0)

    """
    padding = ' ' * indent
    from uio import StringIO
    buffer = StringIO()
    for key in sorted(data.keys()):
        item = data[key]
        value = item['value']
        text = item.get('description', '')
        buffer.write('{}{:<35}{:>25} {:>25}\n'.format(padding, key, value, text))
    return buffer.getvalue()


def _flatten(input_obj, key_prefix, separator='_'):
    """
    Flatten any type of python object into one-level dict object.
    https://github.com/evamayerova/python-flatten/blob/master/flatten_to_dict/flatten_to_dict.py

    :param input_obj: param key_prefix:
    :param key_prefix: 
    :param separator:  (Default value = '_')

    """
    new_dict = {}
    if type(input_obj) is dict:
        for key, value in input_obj.items():
            if type(value) is dict or type(value) is list or type(value) is tuple:
                new_key = key_prefix + key + separator
                new_dict.update(_flatten(input_obj[key], new_key, separator))
            else:
                new_dict[key_prefix + key] = value
    elif type(input_obj) is list or type(input_obj) is tuple:
        for nr, item in enumerate(input_obj):
            new_key = key_prefix + str(nr) + separator
            new_dict.update(_flatten(item, new_key, separator))
    else:
        new_dict[key_prefix[:-1]] = input_obj

    return new_dict


def flatten(input_object, separator='_'):
    """Flatten any object into one-level dict representation.

    :param input_object: 
    :param separator:  (Default value = '_')
    :returns: Flattened object in dict representation.
    Examples:
    https://github.com/evamayerova/python-flatten/blob/master/flatten_to_dict/flatten_to_dict.py
    :rtype: dict

    >>> a = {"f": ["a", "b"], "b": {"x": [1, 2, 3]}, "i": 1}
        >>> flatten(a)
        {
            'f_0': 'a',
            'f_1': 'b',
            'b_x_0': 1,
            'b_x_1': 2,
            'b_x_2': 3,
            'i': 1
         }
    """
    return _flatten(input_object, key_prefix="", separator=separator)


class gc_disabled:
    """Context manager to temporarily disable the garbage collector.
    
    Please be aware this piece does not account for thread safety in any way.
    
    https://community.hiveeyes.org/t/timing-things-on-micropython-for-esp32/2329
    https://bugs.python.org/issue31356
    
    Synopsis::
    
        with gc_disabled():
            # Do something that needs realtime guarantees
            # such as a pair trade, robotic braking, etc.
            run_some_timing_critical_stuff()


    """

    def __enter__(self):
        import gc
        gc.disable()
        return self

    def __exit__(self, *exc_details):
        # exc_info: (<class 'NameError'>, NameError("name 'asdf' is not defined",), None)
        received_exc = exc_details[0] is not None
        import gc
        gc.enable()
        if received_exc:
            raise exc_details[1]


def file_remove(fn: str) -> None:
    """Try to remove a file if it exists.
    
    From logging.handlers.

    :param fn: str: 

    """
    #print('os.remove:', fn)
    try:
        os.remove(fn)
    except OSError:
        pass


def file_exists(fn: str) -> bool:
    """

    :param fn: str: 

    """
    #print('os.stat:', fn)
    try:
        os.stat(fn)
        return True
    except OSError:
        pass
    return False


def ensure_directory(path: str) -> None:
    """

    :param path: str: 

    """
    #print('file_exists')
    if file_exists(path):
        return True
    return os.mkdir(path)


def get_last_stacktrace():
    """ """
    buf = uio.StringIO()
    exc = sys.exc_info()[1]
    sys.print_exception(exc, buf)
    return buf.getvalue()


def random_from_crypto():
    """ """
    platform_info = get_platform_info()
    if platform_info.vendor == platform_info.MICROPYTHON.Pycom:
        # https://forum.pycom.io/topic/1378/solved-how-to-get-random-number-in-a-range/6
        # https://github.com/micropython/micropython-lib/blob/master/random/random.py
        import crypto
        r = crypto.getrandbits(32)
    else:
        import urandom
        r = urandom.getrandbits(32)
    return ((r[0] << 24) + (r[1] << 16) + (r[2] << 8) + r[3]) / 4294967295.0


def randint(a, b):
    """

    :param a: 
    :param b: 

    """
    return random_from_crypto() * (b - a) + a


def backoff_time(n, minimum=1, maximum=600):
    """

    :param n: 
    :param minimum:  (Default value = 1)
    :param maximum:  (Default value = 600)

    """
    # https://en.wikipedia.org/wiki/Exponential_backoff
    # https://cloud.google.com/storage/docs/exponential-backoff
    # https://cloud.google.com/iot/docs/how-tos/exponential-backoff
    # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py
    # https://stackoverflow.com/questions/27438273/exponential-backoff-time-sleep-with-random-randint0-1000-1000
    random_delta = randint(0, 1000) / 1000.0
    delay = min(max((2 ** n) + random_delta, minimum), maximum)
    return delay


class Stopwatch:
    """ """

    def __init__(self):
        self.chronometer = GenericChronometer()
        self.begin = self.chronometer.read()

    def elapsed(self):
        """ """
        return self.chronometer.read() - self.begin

    def reset(self):
        """ """
        self.chronometer.reset()


class PycomChronometer:
    """A chronometer implemented with Pycom MicroPython.
    https://docs.pycom.io/firmwareapi/pycom/machine/timer/


    """

    def __init__(self):
        from machine import Timer
        self.chrono = Timer.Chrono()
        self.chrono.start()

    def read(self):
        """ """
        return self.chrono.read()

    def reset(self):
        """ """
        self.chrono.reset()


class Eggtimer:
    """ """

    def __init__(self, duration):
        self.duration = duration
        self.stopwatch = Stopwatch()

    def expired(self):
        """ """
        return self.stopwatch.elapsed() >= self.duration


def get_platform_info() -> PlatformInfo:
    """ """
    from __main__ import bootloader
    return bootloader.platform_info


def dict_merge(dct, merge_dct, add_keys=True):
    """Recursive dict merge. Inspired by :meth:``dict.update()``, instead of
    updating only top-level keys, dict_merge recurses down into dicts nested
    to an arbitrary depth, updating keys. The ``merge_dct`` is merged into
    ``dct``.
    
    This version will return a copy of the dictionary and leave the original
    arguments untouched.
    
    The optional argument ``add_keys``, determines whether keys which are
    present in ``merge_dict`` but not ``dct`` should be included in the
    new dict.

    :param dct: dict
    :param merge_dct: dict
    :param add_keys: bool (Default value = True)
    :returns: dict: updated dict
    
    Resources:
        https://gist.github.com/angstwad/bf22d1822c38a92ec0a9

    """
    dct = dct.copy()
    if not add_keys:
        merge_dct = {
            k: merge_dct[k]
            for k in set(dct).intersection(set(merge_dct))
        }

    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict)
                and isinstance(merge_dct[k], collections.Mapping)):
            dct[k] = dict_merge(dct[k], merge_dct[k], add_keys=add_keys)
        else:
            dct[k] = merge_dct[k]

    return dct


# Copyright Ferry Boender, released under the MIT license.
# https://www.electricmonk.nl/log/2017/05/07/merging-two-python-dictionaries-by-deep-updating/
def deepupdate(target, src):
    """Deep update target dict with src
    For each k,v in src: if k doesn't exist in target, it is deep copied from
    src to target. Otherwise, if v is a list, target[k] is extended with
    src[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.
    
    Examples:

    :param target: 
    :param src: 

    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print t
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}
    """
    for k, v in src.items():
        if type(v) == list:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                target[k].extend(v)
        elif type(v) == dict:
            if not k in target:
                target[k] = copy.deepcopy(v)
            else:
                deepupdate(target[k], v)
        elif type(v) == set:
            if not k in target:
                target[k] = v.copy()
            else:
                target[k].update(v.copy())
        else:
            target[k] = copy.copy(v)
