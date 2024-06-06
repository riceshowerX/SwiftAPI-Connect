# run.py
from multiprocessing import Process, Pool
from fastapi_server import run_fastapi
from ui.main_ui import run_ui
from app.core.utils.process_monitor import ProcessMonitor
import logging
import signal

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

def signal_handler(sig, frame):
    logging.info("Stopping SwiftAPI-Connect...")
    exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        pool = Pool(processes=2)

        fastapi_process = pool.apply_async(run_fastapi)
        streamlit_process = pool.apply_async(run_ui)

        logging.info(f"Starting FastAPI process with PID: {fastapi_process.pid}")
        logging.info(f"Starting Streamlit process with PID: {streamlit_process.pid}")

        fastapi_monitor = Process(target=ProcessMonitor(fastapi_process.pid, "FastAPI").monitor)
        streamlit_monitor = Process(target=ProcessMonitor(streamlit_process.pid, "Streamlit").monitor)

        fastapi_monitor.start()
        streamlit_monitor.start()

        fastapi_process.wait()
        streamlit_process.wait()

        pool.close()
        pool.join()

    except Exception as e:
        logging.error(f"An error occurred: {e}")