import os
from junit_xml import TestCase, TestSuite

from acre.hooks import logging

from radish import after, world


@after.all()
def after_all(features, marker):
    testcases = []
    for feature in features:
        tid = _get_tid(feature.tags)
        if tid:
            tc = TestCase(id=tid, name=feature.sentence)
        else:
            tc = TestCase(name=feature.sentence)
        for scenario in feature.scenarios:
            if scenario.failed_step:
                tc.add_failure_info(scenario.failed_step.failure.reason, output=scenario.failed_step.failure.traceback)
        testcases.append(tc)
    ts = TestSuite(name=marker, id=logging.trid, test_cases=testcases)
    outfile = os.path.join(world.config.user_data['ARTIFACTS'], f"{logging.trid}-junit.xml")
    fp = open(outfile, "w")
    fp.write(TestSuite.to_xml_string([ts]))
    fp.close()


def _get_tid(tags):
    for tag in tags:
        if tag.name.startswith("tid:"):
            return tag.name

    return None
