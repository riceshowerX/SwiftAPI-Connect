# process_monitor.py
import psutil
import time
import logging
from app.core.config import settings

class ProcessMonitor:
    """监控进程状态"""

    def __init__(self, process_id: int, process_name: str):
        self.process_id = process_id
        self.process_name = process_name

    def monitor(self):
        while True:
            try:
                process = psutil.Process(self.process_id)

                if not process.is_running():
                    logging.warning(f"{self.process_name} is not running!")
                    break

                self.log_resource_usage(process)
                time.sleep(settings.MONITORING_INTERVAL)

            except psutil.NoSuchProcess:
                logging.error(f"Process with ID {self.process_id} not found!")
                break
            except Exception as e:
                logging.error(f"An error occurred while monitoring {self.process_name}: {e}")
                break 

    def log_resource_usage(self, process: psutil.Process):
        """记录资源使用情况"""
        cpu_percent = process.cpu_percent()
        memory_percent = process.memory_percent()

        logging.info(f"{self.process_name} CPU Usage: {cpu_percent}%")
        logging.info(f"{self.process_name} Memory Usage: {memory_percent}%")

        if cpu_percent > settings.CPU_THRESHOLD:
            logging.warning(f"{self.process_name} CPU usage exceeds threshold: {cpu_percent}%")
        if memory_percent > settings.MEMORY_THRESHOLD:
            logging.warning(f"{self.process_name} Memory usage exceeds threshold: {memory_percent}%")