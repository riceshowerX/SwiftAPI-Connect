# process_monitor.py
import psutil
import time
import logging

class ProcessMonitor:
    """监控进程状态"""

    def __init__(self, process_id: int, process_name: str, interval: int = 1, metrics: list = ["cpu", "memory"]):
        self.process_id = process_id
        self.process_name = process_name
        self.interval = interval
        self.metrics = metrics

    def monitor(self):
        while True:
            try:
                process = psutil.Process(self.process_id)
                for metric in self.metrics:
                    if metric == "cpu":
                        cpu_percent = process.cpu_percent()
                        logging.info(f"Process {self.process_name} CPU Usage: {cpu_percent}%")
                    elif metric == "memory":
                        memory_percent = process.memory_percent()
                        logging.info(f"Process {self.process_name} Memory Usage: {memory_percent}%")
                    # 添加其他指标的监控逻辑
            except psutil.ProcessNotFound:
                logging.warning(f"Process {self.process_name} not found")
                break  # 停止监控
            time.sleep(self.interval)

# 示例使用
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
    monitor = ProcessMonitor(process_id=1234, process_name="MyProcess", interval=5, metrics=["cpu", "memory"])
    monitor.monitor()