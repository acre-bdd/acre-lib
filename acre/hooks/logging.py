import time
from acre import log, monitor, Level, userdata, settings, logfile, indent

from radish import before, after, world
from acre.tools import tid


@before.all(order=1)
def setup_logging(features, marker):
    indent.inc()
    log.hint(f"TESTRUN {marker}|{settings.TRID}")


@before.each_feature(order=1)
def before_feature(feature):
    world.tid = tid.tid_from_tags(feature)
    monitor.hint(f"FEATURE: {feature} [{world.tid}]")
    indent.inc()


@after.each_feature
def after_feature(feature):
    indent.dec()


@before.each_scenario
def before_scenario(scenario):
    monitor.hint(f"Scenario: {scenario.sentence}")
    indent.inc()


@after.each_scenario
def after_scenario(scenario):
    indent.dec()
    # monitor.log(_levelByState(scenario.state), f"Scenario: {scenario.sentence}")


@before.each_step
def before_step(step):
    if userdata.delay:
        time.sleep(int(userdata.delay))
    monitor.pending(step.sentence)
    indent.inc()


@after.each_step
def after_step(step):
    indent.dec()
    monitor.log(_levelByState(step.state), step.sentence)
    if "passed" not in step.state:
        monitor.error(step.failure.reason)
        monitor.error(step.failure.traceback)


@after.all
def finish_logging(features, marker):
    log.trace(f"TESTRUN|finished|{marker}|{settings.TRID}")
    log.trace(f"logs written to: {logfile}")
    log.trace(f"check artifacts: {settings.ARTIFACTS}")
    indent.dec()


def _levelByState(state):
    return Level.SUCCESS if "passed" in state else Level.ERROR
