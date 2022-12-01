import os


class Settings:
    def get(self, name, default=None):
        val = self.__getattr__(name)
        return val if val else default

    def __getattr__(self, name):
        if name in os.environ:
            return os.environ[name]


settings = Settings()
