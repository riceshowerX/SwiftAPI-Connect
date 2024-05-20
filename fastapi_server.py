# fastapi_server.py
from app.main import app as fastapi_app
import logging

def run_fastapi():
    import uvicorn
    try:
        logging.info("Starting FastAPI server...")
        uvicorn.run(fastapi_app, host="127.0.0.1", port=8015)
    except Exception as e:
        logging.error(f"An error occurred while running the FastAPI server: {e}")

if __name__ == "__main__":
    run_fastapi()
