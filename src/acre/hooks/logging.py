import os
import logging
from acre import log, userdata, settings

from radish import before, after, world
from acre.tools import tid

levelmap = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'critical': logging.CRITICAL
}

trid = None
logfile = None


@before.all(order=1)
def setup_logging(features, marker):
    global trid
    global logfile
    level = 'info'
    if userdata.loglevel:
        level = userdata.loglevel.lower()

    if level.lower() not in levelmap:
        log.warning(f"Unknown log level '{level}', ignoring")
    else:
        log.console.setLevel(levelmap[level])
        log.debug(f"log level set to: {level}")

    artifacts = settings.ARTIFACTS
    trid = settings.TRID
    logfile = os.path.join(artifacts, f"{trid}.log")
    logfh = logging.FileHandler(os.path.join(artifacts, f"{trid}.log"))
    logfh.setFormatter(logging.Formatter("%(asctime)s|%(levelname)s|%(message)s"))
    logfh.setLevel(log.DEBUG)
    logging.getLogger().addHandler(logfh)
    log.warning(f"{artifacts}/{trid}")
    log.trace(f"testrun {marker} {trid} started")


@before.each_feature
def before_feature(feature):
    world.tid = tid.tid_from_tags(feature.tags)
    log.debug(f"started: {feature} [{world.tid}]")


@after.each_feature
def after_feature(feature):
    log.debug(f"{feature.state}: {feature}")


@before.each_scenario
def before_scenario(scenario):
    log.debug(f"started: Scenario: {scenario.sentence}")


@after.each_feature
def after_scenario(scenario):
    log.debug(f"{scenario.state}: Scenario: {scenario.sentence}")


@before.each_step
def before_step(step):
    log.debug(f"started: Step: {step.sentence}")


@after.each_step
def after_step(step):
    log.debug(f"{step.state}: Step: {step.sentence}")


@after.all
def finish_logging(features, marker):
    global logfile
    log.trace(f"testrun {marker} {trid} finished")
    log.highlight(f"logs written to: {logfile}")
