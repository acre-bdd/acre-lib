import os


class AcrePath:

    def base():
        return os.path.dirname(os.path.dirname(__file__))

    def steps():
        return os.path.join(AcrePath.base(), "steps")
