from configobj import ConfigObj

from radish import world


class Settings:
    def __init__(self):
        self.co = []

    def read(self):
        if 'settings' not in world.config.user_data:
            return

        self.read_settings(world.config.user_data['settings'])

    def read_settings(self, settings):
        sts = settings.split(",")
        for setting in reversed(sts):
            filename = setting.replace(".", "/")
            self.co.append(ConfigObj(f"etc/settings/{filename}"))

    def __getattr__(self, name):
        for co in self.co:
            if name in co:
                return co[name]

        return None


settings = Settings()
settings.read()
