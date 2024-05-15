# run.py
import argparse
import logging
import os
import sys
from uvicorn import Config, Server
from fastapi import FastAPI
from app.main import app as fastapi_app
from app.utils import validate_url

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../app')

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run FastAPI application.")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Host to run the application.")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the application.")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload.")
    parser.add_argument("--workers", type=int, default=1, help="Number of worker processes.")
    parser.add_argument("--ssl", action="store_true", help="Enable SSL.")
    parser.add_argument("--ssl_keyfile", type=str, help="Path to SSL key file.")
    parser.add_argument("--ssl_certfile", type=str, help="Path to SSL certificate file.")
    parser.add_argument("--log_file", type=str, help="Path to log file.")
    parser.add_argument("--log_level", type=str, default="INFO", help="Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).")
    return parser.parse_args()

def configure_logging(log_file, log_level):
    logging.basicConfig(filename=log_file, level=log_level, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    args = parse_arguments()
    configure_logging(args.log_file, args.log_level)

    config = Config(app=fastapi_app, host=args.host, port=args.port, reload=args.reload, workers=args.workers)
    if args.ssl:
        config.ssl_keyfile = args.ssl_keyfile
        config.ssl_certfile = args.ssl_certfile

    server = Server(config)
    server.run()

if __name__ == "__main__":
    main()
