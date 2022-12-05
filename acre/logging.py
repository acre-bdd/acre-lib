import os
import pylogx
from logging import FileHandler, Formatter

from .tools import settings

pylogx.enable_colors()
log = pylogx.log.getChild("acre")

logfh = FileHandler(os.path.join(settings.ARTIFCACTS, f"{settings.TRID}.log"))
logfh.setFormatter(Formatter("%(asctime)s|%(levelname)s|%(message)s"))
logfh.setLevel(log.DEBUG)

logmon = log.getChild("logmon")
logmonfh = FileHandler("/tmp/monitor.log")
logmonfh.setLevel(log.NOTE)
logmonfh.setFormatter(Formatter("%(asctime)s %(indent)s%(message)s"))
logmon.addHandler(logmonfh)

log.addHandler(logfh)

indent = pylogx.IndentFilter()
pylogx.log.addFilter(indent)
pylogx.log.setLevel(pylogx.Level.DEBUG)
