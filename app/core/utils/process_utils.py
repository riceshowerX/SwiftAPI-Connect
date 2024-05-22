# process_utils.py
import psutil
import time
import logging
from multiprocessing import Process

class ProcessMonitor:
    """监控进程状态"""

    def __init__(self, process: psutil.Process, process_name: str, interval: int = 1):
        self.process = process
        self.process_name = process_name
        self.interval = interval

    def monitor(self):
        while True:
            try:
                cpu_percent = self.process.cpu_percent()
                memory_percent = self.process.memory_percent()
                logging.info(f"{self.process_name} - CPU Usage: {cpu_percent:.2f}%, Memory Usage: {memory_percent:.2f}%")
            except psutil.NoSuchProcess:
                logging.warning(f"{self.process_name} process not found, stopping monitor.")
                break
            except Exception as e:
                logging.error(f"An error occurred while monitoring {self.process_name}: {e}")
            time.sleep(self.interval)

    def start(self):
        self.process = Process(target=self.monitor)
        self.process.start()
        logging.info(f"Started monitoring process {self.process_name} with PID: {self.process.pid}")

    def terminate(self):
        if self.process:
            self.process.terminate()
            logging.info(f"Stopped monitoring process {self.process_name}")