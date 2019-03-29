# -*- coding: utf-8 -*-
# (c) 2019 Richard Pobering <richard@hiveeyes.org>
# (c) 2019 Andreas Motl <andreas@hiveeyes.org>
# License: GNU General Public License, Version 3
import logging
from logging import Logger, StreamHandler, Formatter, _level, _loggers

# Keep track of time since boot.
_chrono = None


class TimedLogRecord(logging.LogRecord):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.tdelta = _chrono.read()
        except:
            self.tdelta = None


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
    global _chrono

    # Keep track of time since boot.
    if _chrono is None:
        from machine import Timer
        _chrono = Timer.Chrono()
        _chrono.start()

    if name is None:
        name = "root"
    if name in _loggers:
        return _loggers[name]
    else:
        l = ExtendedLogger(name)
        l.setLevel(level)

        sh = StreamHandler()

        #log_format = '[%(tdelta)s] %(levelname)s %(message)s'
        log_format = '%(tdelta)10.4f [%(name)-21s] %(levelname)-7s: %(message)s'

        sh.setFormatter(Formatter(log_format, style='%'))

        l.addHandler(sh)
    _loggers[name] = l
    return l
