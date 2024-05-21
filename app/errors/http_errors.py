# http_errors.py
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
logger = logging.getLogger(__name__)

class HTTPError(Exception):
    """自定义 HTTP 异常"""

    def __init__(self, status_code: int, detail: str, error_code: str = None, error_message: str = None):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        self.error_message = error_message

    def to_dict(self):
        """将 HTTPError 对象转换为字典格式"""
        return {
            "status_code": self.status_code,
            "detail": self.detail,
            "error_code": self.error_code,
            "error_message": self.error_message,
        }

def http_exception_handler(request: Request, exc: HTTPException):
    """全局 HTTP 异常处理"""
    logger.error(f"HTTP Exception: {exc}")
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
    )