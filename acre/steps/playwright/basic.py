import re

from radish import given, when, then, custom_type, world

from acre import log
from acre.controls import SmartControl


@custom_type('Selector', r'[#][\w_-]+')
def parse_selector(text):
    return text


@custom_type('Word', r'\w+')
def parse_word(text):
    return text


@when('I write {text:QuotedString} to {field:Selector}')
def i_write_text(step, text, field):
    locator = world.page.locator(field)
    locator.fill(text)


@when('I click on the {tag} {text:QuotedString}')
def i_click_on_tag(step, tag, text):
    world.page.get_by_role("link").filter(
        has_text=text).first.click()


@when('I click on the {tag} {field:Selector}')
def i_click_on_tag_field(step, tag, field):
    world.page.locator(field).click()


@when('I click on {field:Selector}')
def i_click_on_field(step, field):
    world.page.locator(field).click()


# @then('I see the {tag:Word} {field:Selector}')
# def i_see_the_tag_selector(step, tag, field):
#     i_see_the_tag(step, tag, field)


@then('I see the {tag:Word} {text:QuotedString}')
def i_see_the_tag_with_text(step, tag, text):
    world.page.get_by_role(tag).filter(
        has_text=text).first.wait_for()


@then('I see the {selector:Selector} {text:QuotedString}')
def i_see_the_selctor_text(step, selector, text):
    world.page.locator(selector).filter(has_text=text).wait_for()


def i_see_the_tag(step, tag=None, field=None, text=None):
    log.note(f"looking up {tag} with {text}")
    world.page.get_by_role(tag, name=re.compile(text)).wait_for()


def _get_locator(field):
    if field.startswith("#"):
        return world.page.get_by_id(field[1:])
    elif field.startswith("@"):
        return world.page.get_by_class(field[1:])
    return world.page.locator(field)


def _get_tag(tag):
    map = {
        "link": "a",
        "heading": "h1",
        "subheading": "h2",
        "paragraph": "p",
    }
    if tag in map:
        return map[tag]
    return tag
