import os


class AcrePath:

    @staticmethod
    def base():
        return os.path.dirname(os.path.dirname(__file__))

    @staticmethod
    def steps():
        return os.path.join(AcrePath.base(), "steps")
