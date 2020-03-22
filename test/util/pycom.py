# -*- coding: utf-8 -*-
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# (c) 2020 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
nvram = {}


def nvs_set(key, value):
    nvram[key] = value


def nvs_get(key):
    if key not in nvram:
        raise KeyError('"{}" not in NVRAM'.format(key))
    return nvram.get(key)


def heartbeat_on_boot(enabled):
    pass


def heartbeat(enabled):
    pass
