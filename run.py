# run.py

from multiprocessing import Process
from fastapi_server import run_fastapi  # 从 fastapi_server 模块导入 run_fastapi 函数
from ui.app import run_ui  # 从 ui.app 模块导入 run_ui 函数

def run_streamlit():
    run_ui()  # 调用 run_ui 函数启动 Streamlit 应用

if __name__ == "__main__":
    # 创建两个进程，一个运行 FastAPI 服务器，一个运行 Streamlit UI 应用
    fastapi_process = Process(target=run_fastapi)
    streamlit_process = Process(target=run_streamlit)

    # 启动两个进程
    fastapi_process.start()
    streamlit_process.start()

    # 等待两个进程结束
    fastapi_process.join()
    streamlit_process.join()
