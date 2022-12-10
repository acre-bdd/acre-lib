import os
import subprocess
import shutil
import sys
import re

from radish import before, after, world
from acre import settings, log

screensize = "1280x1024"
scale = settings.get("VR_SCALE", "800:600,setsar=1:1")
scaling = ["-video_size", screensize, "-vf", f"scale={scale}"]


class VideoRecorder:

    def __init__(self):
        self.vr = None

    def start(self):
        # tid = world.tid.replace(":", "")
        tid = world.tid
        self.vrfile = os.path.join(settings.ARTIFACTS, f"{settings.TRID}-{tid}-video")
        logfile = open(f"{self.vrfile}.log", "w")

        ffmpeg = shutil.which("ffmpeg")
        if not ffmpeg:
            log.warning("ffmpeg not found, skipping video recording")
            return

        cmd = [ffmpeg]
        cmd.extend(Args.get())
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
        if not self.vr:
            log.warning("videorecording seems not to be running")
            return

        if self.vr.returncode:
            log.warning(f"videorecording terminated early with exit code {self.vr.returncode}, check logfile:")
            log.warning(f"{self.vrfile}.log")
            return
        self.vr.terminate()
        self.vr.wait()
        if self.vr.returncode != 255:
            log.warning(f"videorecording terminated with error {self.vr.returncode}, check logfile:")
            log.warning(f"{self.vrfile}.log")
        log.trace(f"vr finished, video: {self.vrfile}.mp4")
        self.vr = None


class Args:
    @staticmethod
    def get():
        args = Args._get_input_args()
        args.extend(["-y", "-pix_fmt", "yuv420p",
                     "-codec:v", "libx264", "-r", "10", "-crf", "38", "-preset", "ultrafast"])
        return args

    @staticmethod
    def _get_input_args():
        if sys.platform == "darwin":
            return ["-f", "avfoundation", "-i", Args._get_mac_capture_device()]
        elif sys.platform == "nt":
            raise Exception("video recording not supported on windows yet")
        else:
            return ["-f", "x11grab", "-i", os.environ["DISPLAY"]]

    @staticmethod
    def _get_mac_capture_device():
        output = subprocess.check_output(
            'ffmpeg -f avfoundation -list_devices true -i "" 2>&1; echo ok', shell=True).decode()
        for line in output.split("\n"):
            m = re.match(r"\[.*\] \[(\d)\] Capture screen", line)
            if m:
                log.warn(f"returning {m.group(1)}")
                return m.group(1)
        raise Exception("Scren capture device not found")


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
