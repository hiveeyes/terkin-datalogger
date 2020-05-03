# -*- coding: utf-8 -*-
# (c) 2020 Andreas Motl <andreas.motl@terkin.org>
# (c) 2020 Jan Hoffmann <jan.hoffmann@bergamsee.de>
# (c) 2020 Richard Pobering <richard@hiveeyes.org>
# License: GNU General Public License, Version 3
import os
import sys
import logging

log = logging.getLogger()


def configure_pythonpath(search_paths):
    sys.path = aslist(search_paths) + sys.path


def patch_system():
    # Fix: RuntimeError: Click will abort further execution because Python 3
    #      was configured to use ASCII as encoding for the environment.
    os.environ['LANG'] = 'en_US.UTF-8'

    # Make environment compatible with CPython.
    log.info('Setting up CPython compatibility layer')
    from terkin_cpython.compat import monkeypatch_cpython
    monkeypatch_cpython()


def setup_logging():
    """
    Configure CPython logger.
    """
    import sys
    import logging
    log_format = '%(asctime)-15s [%(name)-30s] %(levelname)-7s: %(message)s'
    logging.basicConfig(
        format=log_format,
        stream=sys.stderr,
        level=logging.INFO)


def start_bootloader():
    """
    Invoke bootloader.
    """
    import sys
    from umal import MicroPythonBootloader
    bootloader = MicroPythonBootloader()
    sys.modules['__main__'].bootloader = bootloader
    return bootloader


def load_settings(settings_file):

    log.info('Loading settings from "{}"'.format(settings_file))

    # Sanity checks.
    if not os.path.exists(settings_file):
        raise FileNotFoundError('Settings file "{}" not found'.format(settings_file))

    # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path/67692#67692
    import importlib.util
    spec = importlib.util.spec_from_file_location("settings", settings_file)
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    return settings


def aslist(obj, sep=None, strip=True):
    """
    # (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
    # Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php
    """
    if isinstance(obj, str):
        lst = obj.split(sep)
        if strip:
            lst = [v.strip() for v in lst]
        return lst
    elif isinstance(obj, (list, tuple)):
        return obj
    elif obj is None:
        return []
    else:
        return [obj]
