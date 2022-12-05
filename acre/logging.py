import os
import pylogx
from pylogx import Level, log, ColorFormatter
from logging import FileHandler, Formatter, getLevelName, getLogger

from .tools.settings import settings

indent = pylogx.Indent()
pylogx.levels[Level.DEBUG]['attrs'] = ['bold']

level = getLevelName(settings.get('LOG_LEVEL', 'NOTE'))

console = pylogx.enable_colors(level=level, fmt="%(indent)s%(message)s", ups=[Level.NOTE])

logfile = os.path.join(settings.ARTIFACTS, f"{settings.TRID}.log")
logfh = FileHandler(logfile)
logfh.setFormatter(Formatter("{asctime} | {levelname:8} |{indent}{message}", style="{"))
logfh.setLevel(Level.DEBUG)

cf = ColorFormatter(fmt="%(asctime)s %(indent)s%(message)s")
logmon = FileHandler("/tmp/monitor.log")
logmon.setLevel(level)
logmon.setFormatter(cf)

monitor = log.getChild("monitor")
monitor.addHandler(logfh)
monitor.setLevel(Level.DEBUG)
monitor.propagate = False
monitor.addHandler(logmon)

getLogger().addHandler(logfh)
getLogger().addHandler(logmon)
getLogger().addHandler(console)
# getLogger().setLevel(Level.DEBUG)

log.debug(f"log level set to: {level}")
