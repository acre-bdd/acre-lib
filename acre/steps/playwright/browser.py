# -*- coding: utf-8 -*-
from radish import given, then, when, step
from radish import world

from acre import log


@given("I start the browser")
def i_start_the_browser(step):
    world.browser = world.playwright.chromium.launch(headless=False)
    world.page = None


@step("I close the browser")
def i_close_the_browser(step):
    world.browser.close()
    world.browser = None


@when('I navigate to "{url}"')
def i_navigate_to(step, url):
    if not world.browser:
        i_start_the_browser(step)
    if not world.page:
        world.page = world.browser.new_page()
    log.note(f"opening url '{url}'")
    world.page.goto(url)


@then('the page title contains {text:QuotedString}')
def page_title_contains(step, text):
    assert text in world.page.title()
