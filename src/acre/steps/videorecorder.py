import os
import subprocess

from radish import before, after, world
from acre import settings, log

screensize = "1280x1024"
scale = settings.get("VR_SCALE", "800:-1,setsar=1:1")
scaling = ["-video_size", screensize, "-vf", f"scale={scale}"]
args = ["-y", "-f", "x11grab", "-i", os.environ["DISPLAY"], "-pix_fmt", "yuv420p",
        "-codec:v", "libx264", "-r", "10", "-crf", "38", "-preset", "ultrafast"]


class VideoRecorder:

    def __init__(self):
        self.vr = None

    def start(self):
        tid = world.tid.replace(":", "")
        self.vrfile = os.path.join(settings.ARTIFACTS, f"{settings.TRID}-{tid}-video")
        logfile = open(f"{self.vrfile}.log", "w")

        cmd = ["/usr/bin/ffmpeg"]
        cmd.extend(args)
        cmd.extend(scaling)
        cmd.append(f"{self.vrfile}.mp4")
        log.debug(f"vr: {' '.join(cmd)}")
        if self.vr:
            log.warning("video recording already running")
            return
        log.debug(f"starting video recording to {self.vrfile}.mp4")
        self.vr = subprocess.Popen(cmd, stdout=logfile, stderr=logfile)

    def stop(self):
        log.debug(f"stopping video recording for {world.tid}")
        if self.vr.returncode:
            log.warning(f"videorecording terminated early with exit code {self.vr.returncode}, check logfile:")
            log.warning(f"{self.vrfile}.log")
            return
        self.vr.terminate()
        self.vr.wait()
        if self.vr.returncode != 255:
            log.warning(f"videorecording terminated with error {self.vr.returncode}, check logfile:")
            log.warning(f"{self.vrfile}.log")
        log.highlight(f"vr finished, video: {self.vrfile}.mp4")
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
    if settings.VR == "no":
        log.debug("Videorecording disabled")
        return
    world.vr.stop()
