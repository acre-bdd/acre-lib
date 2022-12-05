from radish import given, when, then, custom_type

from acre import log
from acre.controls import SmartControl, Input
from acre.steps.errors import StepError


@custom_type('Selector', r'[#@][\w_-]+')
def parse_selector(text):
    return text


@custom_type('Word', r'\w+')
def parse_word(text):
    return text


@when('I write "{text}" to {field}')
def i_write_text(step, text, field):
    kwargs = _get_kwargs(field)
    selector = Input(**kwargs)
    selector.input(text, enter=True)


@when('I click on the {tag} {field:QuotedString}')
def i_click_on_tag(step, tag, field):
    log.debug(f"i_click_on_the_tag({tag}, {field})")
    kwargs = _get_kwargs(field)
    kwargs['tag'] = _get_tag(tag)
    selector = SmartControl(**kwargs)
    selector.click()


@when('I click on {field:Selector}')
def i_click_on_field(step, field):
    kwargs = _get_kwargs(field)
    button = SmartControl(**kwargs)
    button.click()


@then('I see the {tag:Word} {field:Selector}')
def i_see_the_tag_selector(step, tag, field):
    i_see_the_tag(step, tag, field)


@then('I see the {tag:Word} {text:QuotedString}')
def i_see_the_tag_with_text(step, tag, text):
    i_see_the_tag(step, tag=tag, text=text)


@then('I see the {tag:Word} {selector:Selector} {text:QuotedString}')
def i_see_the_tag_selctor_text(step, tag, selector, text):
    i_see_the_tag(step, tag=tag, field=selector, text=text)


@then('I see the {selector:Selector} {text:QuotedString}')
def i_see_the_selctor_text(step, selector, text):
    i_see_the_tag(step, field=selector, text=text)


def i_see_the_tag(step, tag=None, field=None, text=None):
    kwargs = {}
    if field:
        kwargs.update(_get_kwargs(field))
    if tag:
        kwargs['tag'] = _get_tag(tag)
    if text:
        kwargs['text'] = text
    selector = SmartControl(**kwargs)
    selector.locate()


def _get_kwargs(field):
    kwargs = {}
    if field.startswith("#"):
        kwargs['id'] = field[1:]
    elif field.startswith("@"):
        kwargs['_class'] = field[1:]
    else:
        kwargs['text'] = field[1:-1]
    log.debug(f"_get_kwargs: {kwargs}")
    return kwargs


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
