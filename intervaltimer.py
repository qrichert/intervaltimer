import time
from threading import Event, Thread
from typing import Callable


class IntervalTimer:
    """
    Run callback at given interval, accounting for drift.
    """

    def __init__(self, interval: float, callback: Callable) -> None:
        """
        :param interval: How long to wait between calls (in seconds).
        :param callback: Function or method called at given interval.
        """
        self.interval: float = interval
        self.callback: Callable = callback

        #: Run timer thread as daemon? (must be set before ``start()``).
        self.daemon = False
        #: Used for requesting timer to stop.
        self._exit_flag: Event = Event()
        #: Timestamp of current timer start (or ``None`` if not running).
        self.start_time: float | None = None

    @property
    def is_running(self) -> bool:
        """
        Whether the timer is currently running or not.
        """
        return self.start_time is not None

    def _run(self) -> None:
        """
        Main timer loop.
        """
        # Setup
        self.start_time = time.time()
        # Run
        while not self._exit_flag.is_set():
            self.callback()
            # Adjust next interval delay to account for drift.
            drift: float = (time.time() - self.start_time) % self.interval
            self._exit_flag.wait(self.interval - drift)
        # Reset
        self._exit_flag.clear()
        self.start_time = None

    def start(self) -> None:
        """
        Start timer.
        """
        if self.is_running:
            raise RuntimeError("Timer already started.")
        thread = Thread(target=self._run)
        thread.daemon = self.daemon
        thread.start()

    def stop(self) -> None:
        """
        Request timer to stop (there may be a slight delay).
        """
        if self.is_running:
            self._exit_flag.set()


if __name__ == "__main__":

    def callback():
        print(time.time())

    timer = IntervalTimer(1, callback)
    timer.daemon = True

    print("Run for 10s...")
    timer.start()
    time.sleep(10)
    timer.stop()
    print("Done.")
