import time

from radish import world

from acre import retry
from acre.playwright import TimeoutError


class SmartLocator:
    def __init__(self, name=None, locator=None, parent=None):
        self.name = name
        self._locator = locator
        self._parent = parent

    def locator(self):
        if self._locator:
            return self._locator
        return self.parent().locator(self.name)

    def parent(self):
        if self._parent:
            if isinstance(self._parent, SmartLocator):
                return self._parent.locator()
            return self._parent
        return world.page

    def wait_for(self, *args, **kwargs):
        self.locator().wait_for(*args, **kwargs)

    def exists(self, *args, timeout=5000, **kwargs):
        try:
            self.locator().first.wait_for(*args, timeout=timeout, **kwargs)
            return True
        except TimeoutError:
            return False

    def click(self):
        self.locator().click()

    def clear(self, timeout=1):
        retry(fnc=lambda: not self.exists(timeout=timeout), message=f"clear(): {str(self)}")
        time.sleep(0.2)

    def __str__(self):
        if self.name:
            return f"SmartLocator({self.name})"
        if self._locator:
            return str(self.locator)
        return "SmartLocator"
