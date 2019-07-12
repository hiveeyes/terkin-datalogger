# -*- coding: utf-8 -*-
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3


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


def format_mac(mac_address):
    return ":".join(str_grouper(2, mac_address))
