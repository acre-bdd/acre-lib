import os
import logging as log
from configparser import ConfigParser

from radish import before, world


@before.all(order=10)
def read_profile(features, marker):
    if 'profile' in world.config.user_data:
        profilename = world.config.user_data['profile']
    else:
        log.debug("no profile defined, default profile will be loaded")
        profilename = 'default'
    profile = f"etc/profiles/{profilename}"
    if not os.path.isfile(profile):
        if profilename == 'default':
            log.debug("default profile not found, no profile is loaded")
        else:
            log.warning(f"profile '{profile}' not found, profile not loaded")
        return
    cfg = ConfigParser()
    cfg.read(profile)
    world.profile = ConfigMapper(cfg)


class ConfigMapper:
    def __init__(self, config):
        self.config = config

    def __getattr__(self, section):
        if section not in self.config:
            return None

        return SectionReader(self.config[section])


class SectionReader:
    def __init__(self, section):
        self.section = section

    def __getattr__(self, name):
        log.debug("ValueReader __getattr__(name={}) in section {}".format(name, self.section))
        if name not in self.section:
            return None
        return self.section[name]
