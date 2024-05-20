# run.py
from multiprocessing import Process
from fastapi_server import run_fastapi
from ui.app import run_ui
import logging

def run_streamlit():
    run_ui()

if __name__ == "__main__":
    try:
        # 创建两个进程，一个运行 FastAPI 服务器，一个运行 Streamlit UI 应用
        fastapi_process = Process(target=run_fastapi)
        streamlit_process = Process(target=run_streamlit)

        # 启动两个进程
        fastapi_process.start()
        streamlit_process.start()

        # 等待两个进程结束
        fastapi_process.join()
        streamlit_process.join()

    except Exception as e:
        logging.error(f"An error occurred: {e}")
