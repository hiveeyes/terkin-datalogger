nvram = {}


def nvs_get(key):
    if key not in nvram:
        raise KeyError('"{}" not in NVRAM'.format(key))
    return nvram.get(key)


def heartbeat_on_boot(enabled):
    pass


def heartbeat(enabled):
    pass
