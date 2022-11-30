import os
import subprocess

from radish import before, after, world
from acre.tools import settings
from acre import log


class VideoRecorder:
    screensize = "640x480"
    args = "-y -pix_fmt yuv420p -codec:v libx264 -r 10 -crf 38 -preset ultrafast"

    def __init__(self):
        self.vr = None

    def start(self):
        tid = world.tid.replace(":", "")
        self.vrfile = os.path.join(settings.ARTIFACTS, f"{settings.TRID}-{tid}-video")
        logfile = open(f"{self.vrfile}.log", "w")
        cmd = f"ffmpeg -video_size {VideoRecorder.screensize} {VideoRecorder.args} {self.vrfile}.mp4"
        log.debug(f"vr: {cmd}")
        if self.vr:
            log.warning("video recording already running")
            return
        log.debug(f"starting video recording to {self.vrfile}")
        self.vr = subprocess.Popen(cmd, shell=True, stdout=logfile, stderr=logfile)

    def stop(self):
        log.debug(f"stopping video recording for {world.tid}")
        if self.vr.returncode:
            log.warning("videorecording terminated with exit code {self.vr.returncode}, check logfile:")
            log.warning("{self.vrfile}.log")
        self.vr.terminate()
        self.vr.wait()
        if self.vr.returncode:
            log.warning("videorecording terminated with exit code {self.vr.returncode}, check logfile:")
            log.warning("{self.logfile}.log")
        self.vr = None


@before.each_feature
def start_videorecording(feature):
    if settings.VR == "no":
        log.warning("Videorecording disabled")
        return
    world.vr = VideoRecorder()
    world.vr.start()


@after.each_feature
def stop_videorecording(feature):
    if not settings.VR:
        log.debug("Videorecording disabled")
        return
    world.vr.stop()
