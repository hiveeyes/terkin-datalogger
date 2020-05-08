# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import logging
from logging import Logger, StreamHandler, Formatter
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL
from terkin.util import PycomChronometer, get_platform_info
from umal import GenericChronometer


# Keep track of time since boot.
_chrono = None


def get_chronometer():
    """
    Get a timer that counts from boot.
    """
    global _chrono
    if _chrono:
        return _chrono
    platform_info = get_platform_info()
    if platform_info.vendor == platform_info.MICROPYTHON.Pycom:
        _chrono = PycomChronometer()
    else:
        _chrono = GenericChronometer()
    return _chrono


if hasattr(logging, 'NullHandler'):
    NullHandler = logging.NullHandler
else:
    class NullHandler(logging.Handler):
        def handle(self, record):
            pass
    logging.NullHandler = NullHandler


class TimedLogRecord(logging.LogRecord):
    """ 
    Assign a time (since boot) to a log record.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        chrono = get_chronometer()
        try:
            self.tdelta = chrono.read()
        except:
            self.tdelta = 0


class ExtendedLogger(Logger):
    """ """

    def log(self, level, msg, *args):
        """

        :param level: 
        :param msg: 
        :param *args: 

        """
        from logging import _level

        if level >= (self.level or _level):
            record = TimedLogRecord(
                self.name, level, None, None, msg, args, None, None, None
            )

            if self.handlers:
                for hdlr in self.handlers:
                    hdlr.emit(record)


def getLogger(name=None, level=logging.INFO):
    """

    :param name:  (Default value = None)
    :param level:  (Default value = logging.INFO)

    """
    try:
        from logging import _loggers
    except ImportError:
        return logging.getLogger(name=name)

    if name is None:
        name = "root"
    if name in _loggers:
        return _loggers[name]
    else:
        l = ExtendedLogger(name)
        l.setLevel(level)

        sh = StreamHandler()

        #log_format = '[%(tdelta)s] %(levelname)s %(message)s'
        log_format = '%(tdelta)10.4f [%(name)-28s] %(levelname)-7s: %(message)s'

        sh.setFormatter(Formatter(log_format, style='%'))

        l.addHandler(sh)
    _loggers[name] = l
    return l


def noop(*args, **kwargs):
    """

    :param *args: 
    :param **kwargs: 

    """
    return


loggers_backup = {
    'Logger': Logger.log,
    'ExtendedLogger': ExtendedLogger.log,
}


def disable_logging():
    """ 
    Disabe logging.
    """
    Logger.log = noop
    ExtendedLogger.log = noop


def enable_logging():
    """ 
    Enable logging.
    """
    Logger.log = loggers_backup['Logger']
    ExtendedLogger.log = loggers_backup['ExtendedLogger']
