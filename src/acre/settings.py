from configobj import ConfigObj

from radish import world

from acre import log


class Settings:
    def __init__(self):
        self.co = None

    def read(self):
        self.co = []
        if 'settings' not in world.config.user_data:
            return

        self.read_settings(world.config.user_data['settings'])

    def read_settings(self, settings):
        sts = settings.split(",")
        for setting in reversed(sts):
            filename = setting.replace(".", "/")
            sf = f"etc/settings/{filename}"
            log.warning(f"reading settings files: {sf}")
            self.co.append(ConfigObj(sf))

    def __getattr__(self, name):
        if not self.co:
            self.read()

        for co in self.co:
            if name in co:
                return co[name]

        return None


settings = Settings()
