# -*- coding: utf-8 -*-
from selenium import webdriver

from radish import given, then, when, step
from radish import world

from acre import log


@given("I start the browser")
def i_start_the_browser(step):
    world.webdriver = webdriver.Chrome(
        options=world.chrome_options())


@step("I close the browser")
def i_close_the_browser(step):
    world.webdriver.close()


@when('I navigate to "{url}"')
def i_navigate_to(step, url):
    log.note(f"opening url '{url}'")
    world.webdriver.get(url)


@then('I see "{title}" in the page title')
def i_see_the_title(step, title):
    log.note(f"checking title {title}")
    world.asserts.contains(title, world.webdriver.title)
