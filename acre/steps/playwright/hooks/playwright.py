from playwright.sync_api import sync_playwright

from radish import before, after, world

from acre import log


@before.all(order=5)
def setup_playwright(features, marker):
    log.warning("initialising playwright")
    world.playwright = sync_playwright().start()
    world.browser = None
    world.page = None


@after.all(order=5)
def shutdown_playwright(features, marker):
    world.playwright.stop()
