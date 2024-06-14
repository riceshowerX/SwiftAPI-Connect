# request_schema.py
from typing import Dict, Optional, Union, List
from pydantic import BaseModel, Field, field_validator
import validators

class HTTPRequestSchema(BaseModel):
    """
    HTTP 请求模式定义

    :param method: HTTP 方法（如 GET, POST）
    :param url: 请求的 URL
    :param params: 查询参数
    :param headers: 请求头
    :param data: 请求体数据，可以是字符串或字典
    :param json_data: JSON 请求体数据
    :param encoding: 请求体的编码
    """
    method: str = Field(..., description="HTTP 方法", example="GET")
    url: str = Field(..., description="请求 URL", example="https://example.com")
    params: Optional[Dict[str, str]] = Field(default_factory=dict, description="查询参数", example={"key1": "value1", "key2": "value2"})
    headers: Optional[Dict[str, Union[str, List[str]]]] = Field(default_factory=dict, description="请求头", example={"User-Agent": "Mozilla/5.0"})
    data: Optional[Union[str, Dict]] = Field(None, description="请求体数据")
    json_data: Optional[Dict] = Field(None, description="JSON 请求体数据")
    encoding: Optional[str] = Field("utf-8", description="请求体的编码", example="utf-8")

    @field_validator('method', mode='before')
    def method_must_be_valid(cls, value):
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]
        method = value.upper()
        if method not in valid_methods:
            raise ValueError(f"Invalid HTTP method: {method}. Valid methods are: {valid_methods}")
        return method

    @field_validator('url', mode='before')
    def validate_url(cls, value):
        if not validators.url(value):
            raise ValueError("Invalid URL format.")
        return value
