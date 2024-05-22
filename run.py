# run.py
import os

def main():
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 设置工作目录
    os.chdir(project_root)
    # ... 其余代码
from multiprocessing import Process
from fastapi_server import run_fastapi
from ui.main_ui import run_ui
from app.core.utils.process_utils import ProcessMonitor
import logging

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

def main():
    try:
        # 使用 Process 直接创建和管理进程
        fastapi_process = Process(target=run_fastapi)
        streamlit_process = Process(target=run_ui)

        fastapi_process.start()
        streamlit_process.start()

        logging.info(f"Starting FastAPI process with ID: {fastapi_process.pid}")
        logging.info(f"Starting Streamlit process with ID: {streamlit_process.pid}")

        # 监控进程
        fastapi_monitor = ProcessMonitor(fastapi_process, "FastAPI")
        streamlit_monitor = ProcessMonitor(streamlit_process, "Streamlit")
        fastapi_monitor.start()
        streamlit_monitor.start()

        # 等待进程结束
        fastapi_process.join()
        streamlit_process.join()

        fastapi_monitor.terminate()
        streamlit_monitor.terminate()
    except KeyboardInterrupt:
        logging.info("Received KeyboardInterrupt, terminating processes...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        fastapi_monitor.terminate()
        streamlit_monitor.terminate()
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()