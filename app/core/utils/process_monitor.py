# process_monitor.py
import psutil
import time
import logging

class ProcessMonitor:
    """监控进程状态"""

    def __init__(self, process_id: int, process_name: str):
        self.process_id = process_id
        self.process_name = process_name

    def monitor(self):
        while True:
            process = psutil.Process(self.process_id)
            cpu_percent = process.cpu_percent()
            memory_percent = process.memory_percent()
            logging.info(f"{self.process_name} CPU Usage: {cpu_percent}%")
            logging.info(f"{self.process_name} Memory Usage: {memory_percent}%")
            time.sleep(1)