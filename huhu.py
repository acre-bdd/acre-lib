import subprocess
from acre import settings
from acrelib import log
import logging


class XX:
    def get(self, name, value=None):
        #        return f"huhu {name}/{value}"
        return self.__getattr__(name)

    def __getattr__(self, name):
        return name
        # return self.get(name)


fh = logging.FileHandler("huhu.log")
fh.setLevel(log.DEBUG)
logging.getLogger().getChild("acre").addHandler(fh)

xx = XX()
log.debug("debug message")
log.info(xx.get("abc"))
log.info(xx.huhhu)
log.info(settings.get("USER"))
log.warning(subprocess.run("echo user is $USER", shell=True))
logh = logging.getLogger()
logh.warning("hello world")
logging.warning("blablue")
log.critical("crit blabludssfdsf")
log.error("err blabludssfdsf")
log.trace("trace blabludssfdsf")
log.highlight("highlight blabludssfdsf")
log.warning("sffdfs")
log.fatal("blabludssfdsf")
log.warning("should not appear")
