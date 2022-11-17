import os
import logging
from acre import log

from radish import before, after, world

levelmap = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'critical': logging.CRITICAL
}

trid = None


@before.all(order=1)
def setup_logging(features, marker):
    global trid
    logging.basicConfig()
    level = 'info'
    if 'loglevel' in world.config.user_data:
        level = world.config.user_data['loglevel'].lower()

    if level.lower() not in levelmap:
        log.warning(f"Unknown log level '{level}', ignoring")
    else:
        log.setLevel(levelmap[level])
        log.debug(f"log level set to: {level}")

    artifacts = world.config.user_data['ARTIFACTS']
    trid = world.config.user_data['TRID']
    logfile = logging.FileHandler(os.path.join(artifacts, f"{trid}.log"))
    log.addHandler(logfile)
    log.info(f"testrun {marker} {trid} started")


@before.each_feature
def before_feature(feature):
    log.info(f"started: {feature}")


@after.each_feature
def after_feature(feature):
    log.info(f"{feature.state}: {feature}")


@before.each_scenario
def before_scenario(scenario):
    log.info(f"started: Scenario: {scenario.sentence}")


@after.each_feature
def after_scenario(scenario):
    log.info(f"{scenario.state}: Scenario: {scenario.sentence}")


@before.each_step
def before_step(step):
    log.debug(f"started: Step: {step.sentence}")


@after.each_step
def after_step(step):
    log.debug(f"{step.state}: Step: {step.sentence}")


@after.all
def finish_logging(features, marker):
    log.info(f"testrun {marker} {trid} finished")
