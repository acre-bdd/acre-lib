import re

from DevOpsAPI import Api, Step

from radish import after
from acre import log, settings
from acre.tools import tid


api = Api(organization=settings.DEVOPS_ORG,
          project=settings.DEVOPS_PROJECT,
          user=settings.DEVOPS_USER,
          apikey=settings.DEVOPS_APIKEY)


@after.all()
def after_all(features, marker):
    if not _validate_settings():
        log.warning("devops access not configured, skipping devops update")
        return

    for feature in features:
        ftid = tid.tid_from_tags(feature.tags)
        for scenario in feature.scenarios:
            stid = tid.tid_from_tags(scenario.tags)
            rtid = _make_tid(ftid, stid)
            title = f"{rtid}{scenario.sentence}"
            ids = api.WorkItems.find({"System.Title": f"~{rtid}"})
            if len(ids) > 0:
                tc = api.TestCase.get(ids[0])
                tc.Title = title
            else:
                log.warning(f"area is: {settings.DEVOPS_AREA}")
                tc = api.TestCase.create(title=title, area=settings.DEVOPS_AREA)
            tc.Description = "<br>".join(feature.description)
            tc.steps = [Step(_boldify(rs.sentence)) for rs in scenario.steps]
            all_tags = [tag.name for tag in (feature.tags + scenario.tags)]
            tc.Tags = ",".join(all_tags)


tids = {}


def _make_tid(ftid, stid):
    if stid:
        return stid
    if ftid:
        tids[ftid] = tids[ftid] + 1 if ftid in tids else 1
        return f"{ftid}.{tids[ftid]} "
    return ""


def _boldify(step):
    return re.sub(r"^(Given|When|Then)(.*)", r"&lt;b&gt;\1&lt;/b&gt;\2", step)


def _validate_settings():
    required_settings = {
        "org": settings.DEVOPS_ORG,
        "project": settings.DEVOPS_PROJECT,
        "user": settings.DEVOPS_USER,
        "apikey": settings.DEVOPS_APIKEY,
        "area": settings.DEVOPS_AREA
    }

    for (name, value) in required_settings.items():
        if not value:
            log.warning(f"setting DEVOPS_{name.upper()} not set")
            return False
    return True
