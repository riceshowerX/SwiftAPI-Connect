# run.py
from multiprocessing import Process, Pool
from fastapi_server import run_fastapi
from ui.app import run_ui
from app.utils.process_monitor import ProcessMonitor
import logging

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    try:
        # 创建进程池
        pool = Pool(processes=2)

        # 使用进程池运行 FastAPI 服务器和 Streamlit UI 应用
        fastapi_process = pool.apply(run_fastapi)
        streamlit_process = pool.apply(run_streamlit)

        logging.info(f"Starting FastAPI process with ID: {fastapi_process}")
        logging.info(f"Starting Streamlit process with ID: {streamlit_process}")

        # 创建两个监控线程
        fastapi_monitor = Process(target=ProcessMonitor(fastapi_process, "FastAPI").monitor)
        streamlit_monitor = Process(target=ProcessMonitor(streamlit_process, "Streamlit").monitor)

        # 启动监控线程
        fastapi_monitor.start()
        streamlit_monitor.start()

        # 等待两个进程结束
        pool.close()
        pool.join()

    except Exception as e:
        logging.error(f"An error occurred: {e}")