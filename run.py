# run.py
from multiprocessing import Process, Pool
from fastapi_server import run_fastapi
from ui.app import run_ui
import logging
import psutil  # 添加 psutil 库
import time

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

def run_streamlit():
    run_ui()

def monitor_process(process_name, process_id):
    """监控进程状态"""
    while True:
        process = psutil.Process(process_id)
        cpu_percent = process.cpu_percent()
        memory_percent = process.memory_percent()
        logging.info(f"{process_name} CPU Usage: {cpu_percent}%")
        logging.info(f"{process_name} Memory Usage: {memory_percent}%")
        time.sleep(1)

if __name__ == "__main__":
    try:
        # 创建进程池
        pool = Pool(processes=2)

        # 使用进程池运行 FastAPI 服务器和 Streamlit UI 应用
        fastapi_process = pool.apply_async(run_fastapi)
        streamlit_process = pool.apply_async(run_streamlit)

        logging.info(f"Starting FastAPI process with ID: {fastapi_process.get()} ")
        logging.info(f"Starting Streamlit process with ID: {streamlit_process.get()} ")

        # 创建两个监控线程
        fastapi_monitor = Process(target=monitor_process, args=("FastAPI", fastapi_process.get()))
        streamlit_monitor = Process(target=monitor_process, args=("Streamlit", streamlit_process.get()))

        # 启动监控线程
        fastapi_monitor.start()
        streamlit_monitor.start()

        # 等待两个进程结束
        pool.close()
        pool.join()

    except Exception as e:
        logging.error(f"An error occurred: {e}")