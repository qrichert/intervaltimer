import time
from threading import Event, Thread
from typing import Callable


class IntervalTimer:
    """Run callback at given interval, accounting for drift."""

    def __init__(self, interval: float, callback: Callable) -> None:
        """
        :param interval: How long to wait between calls (in seconds).
        :param callback: Function or method called at given interval.
        """
        self.interval: float = interval
        self.callback: Callable = callback

        self._start_time: float | None = None
        self._exit_flag: Event = Event()

    @property
    def is_running(self) -> bool:
        """Return whether the timer is currently running or not."""
        return self._start_time is not None

    def _run(self) -> None:
        self._start_time = time.monotonic()
        while not self._exit_flag.is_set():
            self.callback()
            # Adjust next interval delay to account for drift.
            drift: float = (time.monotonic() - self._start_time) % self.interval
            self._exit_flag.wait(self.interval - drift)
        self._exit_flag.clear()
        self._start_time = None

    def _ensure_is_not_running(self) -> None:
        if self.is_running:
            raise RuntimeError("Timer already started.")

    def start(self) -> None:
        """Start timer."""
        self._ensure_is_not_running()
        self._run()

    def start_threaded(self, daemon: bool = True) -> None:
        """Start timer in separate thread."""
        self._ensure_is_not_running()
        thread = Thread(target=self._run, daemon=daemon)
        thread.start()

    def stop(self) -> None:
        """Request timer to stop (there may be a slight delay)."""
        if self.is_running:
            self._exit_flag.set()


if __name__ == "__main__":
    timer = IntervalTimer(1, lambda: print(time.time()))

    print("Run for 10s...")
    timer.start_threaded()
    time.sleep(10)
    timer.stop()
    print("Done.")
