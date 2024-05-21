# response_schema.py
from typing import Dict, Optional, Union, List
from datetime import datetime

from pydantic import BaseModel, Field, validator

class HTTPResponseSchema(BaseModel):
    """
    HTTP 响应模式定义

    :param status_code: 响应状态码
    :param text: 响应正文内容
    :param headers: 响应头信息
    :param elapsed: 响应时间（秒）
    :param encoding: 响应正文的编码格式
    :param content_type: 响应正文的 MIME 类型
    """

    status_code: int = Field(..., description="响应状态码", example=200)
    text: Optional[Union[str, bytes]] = Field(None, description="响应正文内容")
    headers: Dict[str, Union[str, List[str]]] = Field(..., description="响应头信息")
    elapsed: float = Field(..., description="响应时间（秒）", example=0.5)
    encoding: Optional[str] = Field(None, description="响应正文的编码格式", example="utf-8")
    content_type: Optional[str] = Field(None, description="响应正文的 MIME 类型", example="text/plain")

    @validator('elapsed')
    def elapsed_must_be_positive(cls, value):
        if value <= 0:
            raise ValueError("Elapsed time must be a positive number.")
        return value

    @validator('status_code')
    def status_code_must_be_valid(cls, value):
        if not 100 <= value <= 599:
            raise ValueError("Status code must be between 100 and 599.")
        return value

    def to_dict(self):
        return {
            "status_code": self.status_code,
            "text": self.text,
            "headers": self.headers,
            "elapsed": self.elapsed,
            "encoding": self.encoding,
            "content_type": self.content_type,
        }

    @classmethod
    def from_attributes(cls, response: httpx.Response):
        """
        从 httpx.Response 对象创建 HTTPResponseSchema 对象
        """
        return cls(
            status_code=response.status_code,
            text=response.text,
            headers=response.headers,
            elapsed=response.elapsed.total_seconds(),
            encoding=response.encoding,
            content_type=response.headers.get('content-type'),
        )