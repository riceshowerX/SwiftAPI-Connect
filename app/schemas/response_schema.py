# response_schema.py
from typing import Dict

from pydantic import BaseModel

class HTTPResponseSchema(BaseModel):
    """
    HTTP 响应模式定义

    :param status_code: 响应状态码
    :param text: 响应正文内容
    :param headers: 响应头信息
    :param elapsed: 响应时间（秒）
    """
    status_code: int
    text: str
    headers: Dict[str, str]
    elapsed: float
