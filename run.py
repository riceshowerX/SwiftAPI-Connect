# run.py
import logging
import signal
import multiprocessing
from multiprocessing import Process
import time
from concurrent.futures import ProcessPoolExecutor

from fastapi_server import run_fastapi
from ui.main_ui import run_ui
from app.core.utils.process_monitor import ProcessMonitor

logging.basicConfig(level=logging.INFO)

def signal_handler(sig, frame):
    logging.info("Stopping SwiftAPI-Connect...")
    exit(0)

def start_process(target, name):
    """启动进程并返回进程对象"""
    process = Process(target=target)
    process.start()
    logging.info(f"Starting {name} process with PID: {process.pid}")
    return process

def monitor_process(process, name):
    """监控进程状态，如果进程退出则尝试重启"""
    while True:
        try:
            # 使用信号处理机制监控进程状态
            process.join()
            logging.info(f"{name} process exited.")
            # 尝试重启进程
            process = start_process(target, name)
        except Exception as e:
            logging.exception(f"An error occurred in {name} process: {e}")
        time.sleep(5)  # 等待 5 秒后尝试重启

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # 注册信号处理函数
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        pool_size = multiprocessing.cpu_count()
        logging.info(f"Starting process pool with {pool_size} workers.")

        # 使用进程池运行 FastAPI 和 Streamlit
        with ProcessPoolExecutor(max_workers=pool_size) as executor:
            # 启动 FastAPI 进程
            fastapi_process = executor.submit(start_process, run_fastapi, "FastAPI").result()
            # 启动 Streamlit 进程
            streamlit_process = executor.submit(start_process, run_ui, "Streamlit").result()

            # 使用单独的线程来监控 FastAPI 和 Streamlit 进程
            fastapi_monitor_thread = threading.Thread(target=monitor_process, args=(fastapi_process, "FastAPI"))
            streamlit_monitor_thread = threading.Thread(target=monitor_process, args=(streamlit_process, "Streamlit"))

            fastapi_monitor_thread.start()
            streamlit_monitor_thread.start()

            fastapi_monitor_thread.join()
            streamlit_monitor_thread.join()

    except Exception as e:
        logging.exception(f"An error occurred: {e}")