import os
import subprocess

from radish import before, after, world
from acre.tools import settings
from acre import log


class VideoRecorder:
    screensize = "640x480"
    args = "-y -f x11grab -pix_fmt yuv420p -codec:v libx264 -r 10 -crf 38 -preset ultrafast"

    def __init__(self):
        self.vr = None

    def start(self):
        vrfile = os.path.join(settings.ARTIFACTS, f"{settings.TRID}-{world.tid}-video.mp4")
        cmd = f"ffmpeg -video_size {VideoRecorder.screensize} -i $DISPLAY {VideoRecorder.args} {vrfile}"
        if self.vr:
            return
        log.debug(f"starting video recording to {vrfile}")
        self.vr = subprocess.Popen(cmd, shell=True)

    def stop(self):
        log.debug(f"stopping video recording for {world.tid}")
        self.vr.terminate()
        self.vr.wait()
        self.vr = None


@before.each_feature
def start_videorecording(feature):
    if not settings.VR:
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
