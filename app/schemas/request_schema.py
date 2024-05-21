# request_schema.py
from typing import Dict, Optional, Union, List
from pydantic import BaseModel, AnyUrl, Field, field_validator
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
logger = logging.getLogger(__name__)

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
    url: AnyUrl = Field(..., description="请求 URL", example="https://example.com")
    params: Optional[Dict[str, str]] = Field({}, description="查询参数", example={"key1": "value1", "key2": "value2"})
    headers: Optional[Dict[str, Union[str, List[str]]]] = Field({}, description="请求头", example={"User-Agent": "Mozilla/5.0"})
    data: Optional[str] = Field(None, description="请求体数据")
    json_data: Optional[Dict] = Field(None, description="JSON 请求体数据")
    encoding: Optional[str] = Field("utf-8", description="请求体的编码", example="utf-8")

    @field_validator('method')
    def method_must_be_valid(cls, value):
        """验证 method 属性是否为有效的 HTTP 方法"""
        valid_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"]
        if value.upper() not in valid_methods:
            logger.error(f"Invalid HTTP method: {value}")
            raise ValueError(f"Invalid HTTP method: {value}. Valid methods are: {valid_methods}")
        return value.upper()  # 统一转换为大写

    @field_validator('url')
    def validate_url(cls, value):
        """验证 url 属性是否为有效的 URL"""
        if not value.startswith(("http://", "https://")):
            logger.error(f"Invalid URL: {value}")
            raise ValueError("URL must start with http:// or https://")
        return value