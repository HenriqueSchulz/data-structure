import psutil
import os
import threading

class CPUMonitor:
    '''This class monitors the CPU usage of the current process and keeps track of the peak usage.'''

    def __init__(self):
        self.process = psutil.Process(os.getpid())
        self.peak_cpu = 0
        self.running = True

    def monitor(self):
        while self.running:
            cpu = self.process.cpu_percent(interval=0.1)
            if cpu > self.peak_cpu:
                self.peak_cpu = cpu

    def start(self):
        self.thread = threading.Thread(target=self.monitor)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
        return self.peak_cpu