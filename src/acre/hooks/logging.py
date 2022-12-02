import time
import os
import logging
from termcolor import colored
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
logmon = None


@before.all(order=1)
def setup_logging(features, marker):
    global trid
    global logfile
    global logmon
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
    logmon = logging.getLogger().getChild("logmon")
    logmon.propagate = False
    logmonh = logging.FileHandler(os.path.join(artifacts, "/tmp/monitor2.log"))
    logmonh.setLevel(log.INFO)
    logmonh.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    logmon.addHandler(logmonh)
    logging.getLogger().addHandler(logfh)
    log.warning(f"{artifacts}/{trid}")
    log.trace(f"TESTRUN {marker}|{trid}")
    logmon.info(colored(f"TESTRUN {marker}|{trid}", "magenta"))


@before.each_feature
def before_feature(feature):
    world.tid = tid.tid_from_tags(feature)
    log.debug(f"FEATURE: {feature} [{world.tid}]")
    logmon.info(colored(f"FEATURE: {feature} [{world.tid}]", "white", attrs=['bold']))


@after.each_feature
def after_feature(feature):
    log.debug(f"FEATURE: {feature.state}|{feature}")
    logmon.info(colored(f"FEATURE: {feature.state}|{feature}", "white", attrs=['bold']))


@before.each_scenario
def before_scenario(scenario):
    log.debug(f"    SCENARIO: {scenario.sentence}")
    logmon.info(colored(f"    SCENARIO: {scenario.sentence}", "white", attrs=['bold']))


@after.each_scenario
def after_scenario(scenario):
    log.debug(f"    SCENARIO {scenario.state}: {scenario.sentence}")
    logmon.info(colored(f"    SCENARIO {scenario.state}: {scenario.sentence}", "white", attrs=['bold']))


@before.each_step
def before_step(step):
    if userdata.delay:
        time.sleep(int(userdata.delay))
    log.debug(f"        STEP: {step.sentence}")
    logmon.info(colored(f"        {step.sentence}", "yellow"))


@after.each_step
def after_step(step):
    log.debug(f"        STEP {step.state}:  {step.sentence}")
    color = "green" if "passed" in step.state else "red"
    logmon.info(colored(f"        {step.sentence}", color))


@after.all
def finish_logging(features, marker):
    global logfile
    log.trace(f"TESTRUN|finished|{marker}|{trid}")
    logmon.info(f"TESTRUN|finished|{marker}|{trid}")
    log.highlight(f"logs written to: {logfile}")
