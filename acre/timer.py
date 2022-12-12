import time
import itertools

from acre import log


class Timer:
    timers = dict()
    started = None

    def start(self):
        self.started = time.time()

    def wait(self, seconds, reason=""):
        if not self.started:
            self.start()
        ii = itertools.count()
        log.debug(f"waiting timer for {seconds}s")
        while True:
            remaining = (self.started + seconds) - time.time()
            if remaining < 0:
                return
            iteration = next(ii)
            if iteration % 10 == 0 or remaining < 10:
                log.note(f"remaining wait time: {remaining // 60}m {remaining % 60}s {reason}")
            time.sleep(remaining if remaining < 1 else 1)
