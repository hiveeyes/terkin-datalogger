# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import sys
import logging
from logging import Logger, StreamHandler, Formatter, _level, _loggers
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

# Keep track of time since boot.
from terkin.util import GenericChronometer, PycomChronometer
if sys.platform in ['WiPy', 'LoPy', 'GPy', 'FiPy']:
    _chrono = PycomChronometer()
else:
    _chrono = GenericChronometer()


class TimedLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.tdelta = _chrono.read()
        except:
            self.tdelta = 0


class ExtendedLogger(Logger):

    def log(self, level, msg, *args):
        if level >= (self.level or _level):
            record = TimedLogRecord(
                self.name, level, None, None, msg, args, None, None, None
            )

            if self.handlers:
                for hdlr in self.handlers:
                    hdlr.emit(record)


def getLogger(name=None, level=logging.INFO):

    if name is None:
        name = "root"
    if name in _loggers:
        return _loggers[name]
    else:
        l = ExtendedLogger(name)
        l.setLevel(level)

        sh = StreamHandler()

        #log_format = '[%(tdelta)s] %(levelname)s %(message)s'
        log_format = '%(tdelta)10.4f [%(name)-25s] %(levelname)-7s: %(message)s'

        sh.setFormatter(Formatter(log_format, style='%'))

        l.addHandler(sh)
    _loggers[name] = l
    return l


def noop(*args, **kwargs):
    return


loggers_backup = {
    'Logger': Logger.log,
    'ExtendedLogger': ExtendedLogger.log,
}


def disable_logging():
    Logger.log = noop
    ExtendedLogger.log = noop


def enable_logging():
    Logger.log = loggers_backup['Logger']
    ExtendedLogger.log = loggers_backup['ExtendedLogger']
