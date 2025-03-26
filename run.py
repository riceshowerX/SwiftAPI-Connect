import logging
import signal
import multiprocessing
from multiprocessing import Process
import time
from typing import Callable

from fastapi_server import run_fastapi
from ui.main_ui import run_ui
from app.core.utils.process_monitor import ProcessMonitor

logging.basicConfig(level=logging.INFO)

# 存储子进程引用
child_processes = {}

def signal_handler(sig, frame):
    """优雅地终止所有子进程并退出"""
    logging.info("Received termination signal. Stopping all services...")
    for name, process in child_processes.items():
        if process.is_alive():
            logging.info(f"Terminating {name} process (PID: {process.pid})")
            process.terminate()
            process.join(timeout=5)
    exit(0)

def run_process(target: Callable, name: str) -> None:
    """运行目标函数并监控进程状态"""
    while True:
        try:
            process = Process(target=target, daemon=True)
            process.start()
            logging.info(f"Started {name} process with PID: {process.pid}")
            
            # 注册进程监控
            ProcessMonitor(process.pid, name).monitor()
            
            # 记录进程退出状态
            return_code = process.join()
            logging.warning(f"{name} process exited with code: {return_code}")
            
        except Exception as e:
            logging.exception(f"Critical error in {name} process: {e}")
        
        # 自动重启逻辑
        logging.info(f"Restarting {name} process in 5 seconds...")
        time.sleep(5)

def start_managed_process(target: Callable, name: str) -> Process:
    """启动并管理守护进程"""
    process = Process(target=run_process, args=(target, name), daemon=True)
    process.start()
    return process

if __name__ == "__main__":
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # 启动核心服务
        child_processes["FastAPI"] = start_managed_process(run_fastapi, "FastAPI")
        child_processes["Streamlit"] = start_managed_process(run_ui, "Streamlit")

        # 保持主进程运行
        while True:
            time.sleep(1)

    except Exception as e:
        logging.exception("Main process encountered an error:")
        signal_handler(signal.SIGTERM, None)  # 触发优雅退出