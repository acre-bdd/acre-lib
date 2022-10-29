from radish import world


class Settings:
    def __getattr__(self, name):

        if name not in world.config.user_data:
            return None
        return world.config.user_data[name]


settings = Settings()
