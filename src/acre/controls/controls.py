import logging

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from radish import world

class Control():
    def __init__(self, xpath=None):
        self.xpath = xpath


    def input(self, text):
        self.locate()
        self.match.send_keys(text)

    def locate(self, timeout=30):
        self.timeout = timeout
        logging.debug(f"locating: {self.xpath}")
        self.match = world.webdriver.find_element(By.XPATH, self.xpath)
        return self

    def exists(self, timeout=1):
        try:
            self.locate(timeout)
            return True
        except NoSuchElementException:
            return False

    def click(self):
        self.locate()
        self.match.click()
        return self

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        world.webdriver.implicitly_wait(float(value))


class SmartControl(Control):
    def __init__(self, tag="*", **kwargs):

        filter = []
        filterstr = ""

        for name, value in kwargs.items():
            if name.startswith('_'):
                name = name[1:]
            name = name.replace("_", "-")
            name = "." if name == 'text' else f"@{name}"
            filter.append(f"contains({name}, '{value}')")
        if len(filter) > 0:
            filterstr = f'[{" and ".join(filter)}]'
        super().__init__(f"//{tag}{filterstr}")


class Title(SmartControl):
    def __init__(self, **kwargs):
        super().__init__(tag='h1')


class Input(SmartControl):
    def __init__(self, **kwargs):
        super().__init__(tag='input', **kwargs)


class Link(SmartControl):
    def __init__(self, **kwargs):
        super().__init__(tag='a', **kwargs)


class Div(SmartControl):
    def __init__(self, **kwargs):
        super().__init__(tag="div", **kwargs)


class Button(SmartControl):
    def __init__(self, **kwargs):
        super().__init__(tag="button", **kwargs)
