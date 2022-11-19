import re

from DevOpsAPI import Api, Step

from radish import after
from acre import log, settings


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
        ftid = _get_tid(feature.tags)
        for scenario in feature.scenarios:
            stid = _get_tid(scenario.tags)
            tid = _make_tid(ftid, stid)
            title = f"{tid}{scenario.sentence}"
            log.warning(f"Setting title to {title}")
            ids = api.WorkItems.find({"System.Title": f"~{tid}"})
            if len(ids) > 0:
                tc = api.TestCase.get(ids[0])
                log.warning(f"Setting title to {title}")
                tc.Title = title
            else:
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


def _get_tid(tags):
    for tag in tags:
        if tag.name.startswith("tid:"):
            return tag.name

    return None


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
            log.warning(f"setting DEVOPS_{name.upper()} not valid")
            return False
    return True
