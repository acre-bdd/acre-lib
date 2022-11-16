import logging as log

from radish import before, world


@before.all(order=1)
def logging(features, marker):
    if 'loglevel' not in world.config.user_data:
        return

    level = world.config.user_data['loglevel'].lower()
    levelmap = {
        'debug': log.DEBUG,
        'info': log.INFO,
        'warning': log.WARNING,
        'critical': log.CRITICAL
    }
    if level.lower() not in levelmap:
        log.warning(f"Unknown log level '{level}', ignoring")
        return
    log.debug(f"setting log level: {level}")
    log.basicConfig(level=levelmap[level])
