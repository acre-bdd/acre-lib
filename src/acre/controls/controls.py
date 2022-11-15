from selenium.webdriver.common.by import By

from radish import world


class Control():
    def __init__(self, tag="*", id=None, cssclass=None, text=None, **kwargs):
        filter = []
        filterstr = ""

        if id:
            filter.append(f"contains(@id, '{id}')")
        if cssclass:
            filter.append(f"contains(@class, '{cssclass}')")
        if text:
            filter.append(f"contains(., '{text}')")
        for name, value in kwargs:
            filter.append(f"contains(@{name}, '{value}')")
        if len(filter) > 0:
            filterstr = f'[{" and ".join(filter)}]'
        self.xpath = f"//{tag}{filterstr}"

    def input(self, text):
        self.locate()
        self.match.send_keys(text)

    def locate(self, timeout=30):
        self.timeout = timeout
        self.match = world.webdriver.find_element(By.XPATH, self.xpath)

    def click(self):
        self.locate()
        self.match.click()

    @property
    def timeout(self):
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        world.webdriver.implicitly_wait(float(value))


class Title(Control):
    def __init__(self, id=None, cssclass=None, text=None):
        super().__init__(tag='h1', id=id, cssclass=cssclass, text=text)


class Input(Control):
    def __init__(self, id=None, cssclass=None, text=None):
        super().__init__(tag='input', id=id, cssclass=cssclass, text=text)


class Link(Control):
    def __init__(self, id=None, cssclass=None, text=None):
        super().__init__(tag='a', id=id, cssclass=cssclass, text=text)
