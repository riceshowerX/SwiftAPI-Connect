import psutil
import time
import logging
from app.core.config import settings
from typing import Optional

class ProcessMonitor:
    """增强型进程监控类"""

    def __init__(self, process_id: int, process_name: str):
        self.process_id = process_id
        self.process_name = process_name
        self._process = None  # 缓存进程对象

    def monitor(self) -> None:
        """主监控循环"""
        logging.info(f"Starting monitoring for {self.process_name} (PID: {self.process_id})")
        
        while self._is_process_valid():
            try:
                self._process = psutil.Process(self.process_id)
                self._check_resource_usage()
                time.sleep(settings.MONITORING_INTERVAL)
                
            except psutil.NoSuchProcess:
                logging.error(f"监控终止：进程 {self.process_id} 已不存在")
                break
            except psutil.AccessDenied:
                logging.error(f"权限不足：无法访问进程 {self.process_id} 的资源信息")
                break
            except Exception as e:
                logging.exception(f"监控异常：{str(e)}")
                break

    def _is_process_valid(self) -> bool:
        """验证进程有效性"""
        if not self.process_id:
            logging.error("无效的进程ID")
            return False
            
        try:
            return psutil.pid_exists(self.process_id)
        except Exception:
            return False

    def _check_resource_usage(self) -> None:
        """执行资源检查并记录"""
        if not self._process.is_running():
            logging.warning(f"进程 {self.process_name} (PID: {self.process_id}) 已停止")
            return

        try:
            with self._process.oneshot():
                cpu_usage = self._process.cpu_percent()
                mem_usage = self._process.memory_percent()
                
                self._log_metrics(cpu_usage, mem_usage)
                self._check_thresholds(cpu_usage, mem_usage)
                
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logging.warning(f"资源检查失败：{str(e)}")

    def _log_metrics(self, cpu: float, memory: float) -> None:
        """记录资源使用指标"""
        log_message = (
            f"监控报告 - {self.process_name} (PID: {self.process_id}) | "
            f"CPU: {cpu:.1f}% | 内存: {memory:.1f}%"
        )
        logging.info(log_message)

    def _check_thresholds(self, cpu: float, memory: float) -> None:
        """检查资源使用阈值"""
        if cpu > settings.CPU_THRESHOLD:
            logging.warning(
                f"CPU阈值警报：{cpu:.1f}% 超过设定阈值 {settings.CPU_THRESHOLD}%"
            )
        if memory > settings.MEMORY_THRESHOLD:
            logging.warning(
                f"内存阈值警报：{memory:.1f}% 超过设定阈值 {settings.MEMORY_THRESHOLD}%"
            )