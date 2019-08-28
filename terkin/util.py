# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import uio


def to_base64(bytes):
    """Encode bytes to base64 encoded string"""
    # TODO: Move to ``util.py``.
    import base64
    return base64.encodebytes(bytes).decode().rstrip()


def format_exception(ex):
    return '{}: {}'.format(ex.__class__.__name__, ex)


def get_device_id():
    import machine
    from ubinascii import hexlify
    return hexlify(machine.unique_id()).decode()


class URI:
    def __str__(self):
        return str(self.__dict__)


def urlparse(url, scheme='', allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
    Return a 6-tuple: (scheme, netloc, path, params, query, fragment).
    Note that we don't break the components up in smaller bits
    (e.g. netloc is a single string) and we don't expand % escapes."""
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
    # https://stackoverflow.com/questions/11006702/elegant-format-for-a-mac-address-in-python-3-2/11006779#11006779
    args = [iter(iterable)] * n
    for part in zip(*args):  # itertools.izip in 2.x for efficiency.
        yield "".join(part)


def format_mac_address(mac_address):
    return ":".join(str_grouper(2, mac_address)).lower()


def dformat(data, indent=0):
    padding = ' ' * indent
    from uio import StringIO
    buffer = StringIO()
    for key in sorted(data.keys()):
        value = data[key]
        buffer.write('{}{}: {}\n'.format(padding, key, value))
    return buffer.getvalue()


def ddformat(data, indent=0):
    padding = ' ' * indent
    from uio import StringIO
    buffer = StringIO()
    for key in sorted(data.keys()):
        item = data[key]
        value = item['value']
        text = item.get('description', '')
        buffer.write('{}{:<40}{:>10}    {}\n'.format(padding, key, value, text))
    return buffer.getvalue()


def _flatten(input_obj, key_prefix, separator='_'):
    """
    Flatten any type of python object into one-level dict object.
    https://github.com/evamayerova/python-flatten/blob/master/flatten_to_dict/flatten_to_dict.py

    :param input_obj:
    :param key_prefix:
    :return:
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
    """
    Flatten any object into one-level dict representation.

    Args:
        input_object: Python object (list, dict, tuple, int, string, ...)
    Returns:
        dict: Flattened object in dict representation.
    Examples:
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

    https://github.com/evamayerova/python-flatten/blob/master/flatten_to_dict/flatten_to_dict.py
    """
    return _flatten(input_object, key_prefix="", separator=separator)


class gc_disabled:
    """
    Context manager to temporarily disable the garbage collector.

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
    """
    Try to remove a file if it exists.

    From logging.handlers.
    """
    #print('os.remove:', fn)
    try:
        os.remove(fn)
    except OSError:
        pass


def file_exists(fn: str) -> bool:
    #print('os.stat:', fn)
    try:
        os.stat(fn)
        return True
    except OSError:
        pass
    return False


def ensure_directory(path: str) -> None:
    #print('file_exists')
    if file_exists(path):
        return True
    return os.mkdir(path)


def get_last_stacktrace():
    buf = uio.StringIO()
    exc = sys.exc_info()[1]
    sys.print_exception(exc, buf)
    return buf.getvalue()


def random_from_crypto():
    # https://forum.pycom.io/topic/1378/solved-how-to-get-random-number-in-a-range/6
    # https://github.com/micropython/micropython-lib/blob/master/random/random.py
    import crypto
    r = crypto.getrandbits(32)
    return ((r[0]<<24) + (r[1]<<16) + (r[2]<<8) + r[3]) / 4294967295.0


def randint(a, b):
    """Return random integer in range [a, b], including both end points."""
    return random_from_crypto() * (b - a) + a


def backoff_time(n, minimum=1, maximum=600):
    # https://en.wikipedia.org/wiki/Exponential_backoff
    # https://cloud.google.com/storage/docs/exponential-backoff
    # https://cloud.google.com/iot/docs/how-tos/exponential-backoff
    # https://github.com/GoogleCloudPlatform/python-docs-samples/blob/master/iot/api-client/mqtt_example/cloudiot_mqtt_example.py
    # https://stackoverflow.com/questions/27438273/exponential-backoff-time-sleep-with-random-randint0-1000-1000
    random_delta = randint(0, 1000) / 1000.0
    delay = min(max((2 ** n) + random_delta, minimum), maximum)
    return delay


class Stopwatch:

    def __init__(self):
        self.chronometer = GenericChronometer()
        self.begin = self.chronometer.read()

    def elapsed(self):
        return self.chronometer.read() - self.begin

    def reset(self):
        self.chronometer.reset()


class GenericChronometer:
    """
    A millisecond chronometer implemented with vanilla MicroPython.
    https://micropython.readthedocs.io/en/latest/pyboard/tutorial/timer.html#making-a-microsecond-counter
    """

    def __init__(self):
        import time
        self.start = time.ticks_ms()

    def read(self):
        import time
        return time.ticks_diff(time.ticks_ms(), self.start) / 1000.0

    def reset(self):
        import time
        self.start = time.ticks_ms()


class PycomChronometer:
    """
    A chronometer implemented with Pycom MicroPython.
    https://docs.pycom.io/firmwareapi/pycom/machine/timer/
    """

    def __init__(self):
        from machine import Timer
        self.chrono = Timer.Chrono()
        self.chrono.start()

    def read(self):
        return self.chrono.read()

    def reset(self):
        self.chrono.reset()


class Eggtimer:

    def __init__(self, duration):
        self.duration = duration
        self.stopwatch = Stopwatch()

    def expired(self):
        return self.stopwatch.elapsed() >= self.duration
