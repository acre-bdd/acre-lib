
def tid_from_tags(feature):
    for tag in feature.tags:
        if tag.name.startswith("tid:"):
            return tag.name
    return feature.id
