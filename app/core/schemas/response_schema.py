from typing import Dict, Optional, Union, List
from datetime import datetime
import httpx
from pydantic import BaseModel, Field, validator, HttpUrl, root_validator
from pydantic import model_validator  # Pydantic V2 导入

class HTTPResponseSchema(BaseModel):
    """
    HTTP 响应模式定义

    Attributes:
        status_code: 响应状态码 (100-599)
        text: 响应正文内容
        headers: 响应头信息（支持多值头）
        elapsed: 响应时间（秒）
        encoding: 响应编码格式
        content_type: 响应内容类型
    """
    
    status_code: int = Field(
        ...,
        description="HTTP响应状态码",
        example=200,
        ge=100,
        le=599
    )
    text: str = Field(
        ...,
        description="响应体文本内容",
        example="{'key': 'value'}"
    )
    headers: Dict[str, Union[str, List[str]]] = Field(
        ...,
        description="响应头信息（支持多值头）"
    )
    elapsed: float = Field(
        ...,
        description="请求耗时（秒）",
        example=0.45,
        gt=0
    )
    encoding: Optional[str] = Field(
        default="utf-8",
        description="响应编码格式",
        example="utf-8"
    )
    content_type: Optional[str] = Field(
        default=None,
        description="MIME类型",
        example="application/json"
    )

    @model_validator(mode='after')
    def validate_headers(self) -> 'HTTPResponseSchema':
        """验证并标准化响应头格式"""
        normalized_headers = {}
        for key, value in self.headers.items():
            if isinstance(value, list):
                normalized_headers[key] = [str(v) for v in value]
            else:
                normalized_headers[key] = str(value)
        self.headers = normalized_headers
        return self

    @classmethod
    def from_response(cls, response: httpx.Response) -> 'HTTPResponseSchema':
        """从httpx响应对象创建模式实例"""
        # 处理多值响应头
        headers = {}
        for key, value in response.headers.multi_items():
            if key in headers:
                if isinstance(headers[key], list):
                    headers[key].append(value)
                else:
                    headers[key] = [headers[key], value]
            else:
                headers[key] = value

        return cls(
            status_code=response.status_code,
            text=response.text,
            headers=headers,
            elapsed=response.elapsed.total_seconds(),
            encoding=response.encoding,
            content_type=response.headers.get('content-type')
        )

    def to_dict(self) -> Dict:
        """转换为标准字典格式"""
        return {
            "status_code": self.status_code,
            "text": self.text,
            "headers": self.headers,
            "elapsed": self.elapsed,
            "encoding": self.encoding,
            "content_type": self.content_type,
        }