
def tid_from_tags(tags):
    for tag in tags:
        if tag.name.startswith("tid:"):
            return tag.name

    return None
