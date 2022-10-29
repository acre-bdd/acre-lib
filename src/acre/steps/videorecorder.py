import logging
from datetime import datetime
import os
import time

from subprocess import call

from radish import before, after, world
from acre.tools import settings


log = logging.getLogger()

CMD = 'videorecording'


reportsdir = world.config.user_data['reportsdir'] if 'reportsdir' in world.config.user_data else 'reports/'


class VideoRecorder:

    def __init__(self, name):
        self.started = False
        self.name = name

    def start(self):
        if self.started:
            return
        log.debug(f"starting video recording for {self.name} to {reportsdir}")
        self.started = datetime.now()
        call([CMD,
              "start",
              os.environ["DISPLAY"],
              reportsdir,
              # 'reports/',
              self.name])
        self.subtitles.startofvideo = self.started

    def stop(self):
        log.debug(f"stopping video recording for {self.name}")
        self.started = False
        call([CMD,
              "stop",
              os.environ["DISPLAY"],
              reportsdir,
              self.name])


@before.each_feature
def start_videorecording(feature):
    if not settings.VR:
        log.debug("Videorecording disabled")
        return
    fn = _feature2name(feature)
#   print(feature.line)
#   print(feature.sentence)
#   print(feature.keyword)
#   print(feature.description)
#   print(feature.path)
    log.debug(f"start video recording for '{fn}'")
    world.vr = VideoRecorder(fn)
    world.vr.start()
    world.vr.feature = fn
    world.vr.subtitles.start("feature: " + _feature2name(feature))


@after.each_feature
def stop_videorecording(feature):
    if not settings.VR:
        log.debug("Videorecording disabled")
        return
    fn = _feature2name(feature)
    log.debug(f"stop video recording for '{fn}'")
    if not world.vr or not world.vr.started:
        return
    world.vr.subtitles.start("{feature.state} feature: {fn}")
    time.sleep(1)
    world.vr.subtitles.stop()
    world.vr.stop()


def _feature2name(feature):
    return os.path.basename(feature.path)


def _formatdelta(timedelta):
    # return timedelta.strftime("%H:%M:%S,%fff")
    TFT = "%02d:%02d:%02d,%03d"
    return TFT % (
        timedelta.seconds // 3600,
        timedelta.seconds % 3600 // 60,
        timedelta.seconds % 3600 % 60,
        timedelta.microseconds // 1000)


def _colorize(color, text):
    # return '<font color={}>x{}</font>'.format(color, text)
    return text


def _orange(text):
    return _colorize("#999922", text)


def _blue(text):
    return _colorize("#2222ee", text)
