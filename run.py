from multiprocessing import Process
from fastapi_server import run_fastapi  # 从单独模块导入
from ui.app import run_ui

def run_streamlit():
    run_ui()  # 调用 run_ui 函数

if __name__ == "__main__":
    fastapi_process = Process(target=run_fastapi)
    streamlit_process = Process(target=run_streamlit)

    fastapi_process.start()
    streamlit_process.start()

    fastapi_process.join()
    streamlit_process.join()