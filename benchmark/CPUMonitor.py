import psutil
import os
import threading


class CPUMonitor:
    '''Monitors CPU usage of the current process and records the peak usage.'''

    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.peak_cpu = 0.0
        self.stop_event = threading.Event()
        self.thread = None

    def monitor(self):

        # warm-up call required by psutil
        self.process.cpu_percent(None)

        while not self.stop_event.is_set():

            cpu = self.process.cpu_percent(interval=0.1)

            if cpu > self.peak_cpu:
                self.peak_cpu = cpu

    def start(self):

        self.peak_cpu = 0.0
        self.stop_event.clear()

        self.thread = threading.Thread(target=self.monitor, daemon=True)
        self.thread.start()

    def stop(self):

        self.stop_event.set()

        if self.thread:
            self.thread.join()

        return self.peak_cpu