# run.py
from multiprocessing import Process, Pool
from fastapi_server import run_fastapi
from ui.app import run_ui  # 从 ui.UI.py 文件中导入 run_ui 函数 
from app.utils.process_monitor import ProcessMonitor
import logging
import time

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

def run_monitor(process_id, process_name):
    """运行进程监控"""
    monitor = ProcessMonitor(process_id, process_name)
    monitor.monitor()

if __name__ == "__main__":
    try:
        # 创建进程池
        pool = Pool(processes=2)

        # 使用进程池运行 FastAPI 服务器和 Streamlit UI 应用
        fastapi_process = pool.apply_async(run_fastapi)
        streamlit_process = pool.apply_async(run_ui)  # 使用导入的 run_ui 函数

        logging.info(f"Starting FastAPI process...")
        logging.info(f"Starting Streamlit process...")

        # 创建两个监控线程
        fastapi_monitor = Process(target=run_monitor, args=(fastapi_process.pid, "FastAPI"))
        streamlit_monitor = Process(target=run_monitor, args=(streamlit_process.pid, "Streamlit"))

        # 启动监控线程
        fastapi_monitor.start()
        streamlit_monitor.start()

        # 等待两个进程结束
        pool.close()
        pool.join()

        # 停止监控线程
        fastapi_monitor.join()
        streamlit_monitor.join()

    except Exception as e:
        logging.error(f"An error occurred: {e}")