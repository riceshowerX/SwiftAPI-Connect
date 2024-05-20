# fastapi_server.py
from app.main import app as fastapi_app

def run_fastapi():
    import uvicorn
    uvicorn.run(fastapi_app, host="127.0.0.1", port=8015)