# run.py
import logging
import signal
import multiprocessing
from multiprocessing import Process
import time

from fastapi_server import run_fastapi
from ui.main_ui import run_ui
from app.core.utils.process_monitor import ProcessMonitor

logging.basicConfig(level=logging.INFO)

def signal_handler(sig, frame):
    logging.info("Stopping SwiftAPI-Connect...")
    exit(0)

def start_process(target, name):
    """启动进程并返回进程对象"""
    try:
        process = Process(target=target)
        process.start()
        logging.info(f"Starting {name} process with PID: {process.pid}")
        return process
    except Exception as e:
        logging.exception(f"Failed to start {name} process: {e}")
        return None

def monitor_process(process, name):
    """监控进程状态，如果进程退出则尝试重启"""
    monitor = ProcessMonitor(process, name)
    monitor.start()
    monitor.join()  # 等待监控进程结束

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # 注册信号处理函数
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # 启动 FastAPI 进程
        fastapi_process = start_process(run_fastapi, "FastAPI")
        if fastapi_process is None:
            exit(1)

        # 启动 Streamlit 进程
        streamlit_process = start_process(run_ui, "Streamlit")
        if streamlit_process is None:
            exit(1)

        # 启动监控进程
        fastapi_monitor_process = Process(target=monitor_process, args=(fastapi_process, "FastAPI"))
        streamlit_monitor_process = Process(target=monitor_process, args=(streamlit_process, "Streamlit"))

        fastapi_monitor_process.start()
        streamlit_monitor_process.start()

        fastapi_monitor_process.join()
        streamlit_monitor_process.join()

    except Exception as e:
        logging.exception(f"An error occurred: {e}")