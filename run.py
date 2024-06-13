# run.py
import logging
import signal
import multiprocessing
from multiprocessing import Process, Pool
import time

from fastapi_server import run_fastapi
from ui.main_ui import run_ui
from app.core.utils.process_monitor import ProcessMonitor

logging.basicConfig(level=logging.INFO)

def signal_handler(sig, frame):
    logging.info("Stopping SwiftAPI-Connect...")
    exit(0)

def run_process(target, name):
    """运行进程并监控其状态，如果进程退出则尝试重启"""
    while True:
        try:
            process = Process(target=target)
            process.start()
            logging.info(f"Starting {name} process with PID: {process.pid}")
            ProcessMonitor(process.pid, name).monitor()  # 监控进程
        except Exception as e:
            logging.exception(f"An error occurred in {name} process: {e}")
        time.sleep(5)  # 等待 5 秒后尝试重启

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        pool_size = multiprocessing.cpu_count()
        logging.info(f"Starting process pool with {pool_size} workers.")

        # 使用进程池运行 FastAPI 和 Streamlit
        with Pool(processes=pool_size) as pool:
            pool.apply_async(run_process, args=(run_fastapi, "FastAPI"))
            pool.apply_async(run_process, args=(run_ui, "Streamlit"))

            pool.close()
            pool.join()

    except Exception as e:
        logging.exception(f"An error occurred: {e}")