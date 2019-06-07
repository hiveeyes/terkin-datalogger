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
