# flake8: noqa: F401
import pylogx
from acre.tools.settings import settings
from acre.tools.userdata import userdata

pylogx.enable_colors()
log = pylogx.log.getChild("acre")
pylogx.log.setLevel(pylogx.Level.DEBUG)
