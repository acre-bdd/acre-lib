
from radish import world

from acre.playwright import TimeoutError


class SmartLocator:
    def __init__(self, name=None):
        self.name = name

    def locator(self):
        return world.page.locator(self.name)

    def wait_for(self, *args, **kwargs):
        self.locator().wait_for(*args, **kwargs)

    def exists(self, *args, timeout=5000, **kwargs):
        try:
            self.locator().wait_for(*args, timeout=timeout, **kwargs)
            return True
        except TimeoutError:
            return False
