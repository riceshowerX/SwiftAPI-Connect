from multiprocessing import Process
from app.main import app as fastapi_app
from ui.app import run_ui  # 导入 run_ui 函数

def run_fastapi():
    import uvicorn
    uvicorn.run(fastapi_app, host="127.0.0.1", port=821101)

def run_streamlit():
    run_ui()  # 调用 run_ui 函数

if __name__ == "__main__":
    fastapi_process = Process(target=run_fastapi)
    streamlit_process = Process(target=run_streamlit)

    fastapi_process.start()
    streamlit_process.start()

    fastapi_process.join()
    streamlit_process.join()