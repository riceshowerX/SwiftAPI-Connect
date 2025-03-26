from typing import Dict, Optional, Union, List
from pydantic import BaseModel, Field, field_validator, ValidationError
import validators

class HTTPRequestSchema(BaseModel):
    """
    HTTP请求模式定义

    Attributes:
        method: HTTP方法（GET/POST等）
        url: 请求URL
        params: 查询参数字典
        headers: 请求头字典
        data: 原始请求体数据（字符串或字典）
        json_data: JSON格式的请求体数据
        encoding: 请求体编码方式
    """
    
    method: str = Field(
        ...,
        description="HTTP方法",
        example="GET",
        regex=r"^(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS|CONNECT|TRACE)$"
    )
    
    url: AnyUrl = Field(
        ...,
        description="请求URL",
        example="https://example.com"
    )
    
    params: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="URL查询参数",
        example={"page": "1", "sort": "asc"}
    )
    
    headers: Optional[Dict[str, Union[str, List[str]]]] = Field(
        default_factory=dict,
        description="HTTP请求头",
        example={"Accept": "application/json"}
    )
    
    data: Optional[Union[str, Dict]] = Field(
        default=None,
        description="原始请求体数据"
    )
    
    json_data: Optional[Dict] = Field(
        default=None,
        description="JSON格式的请求体数据"
    )
    
    encoding: Optional[str] = Field(
        default="utf-8",
        description="请求体编码方式",
        example="utf-8"
    )

    @field_validator('method')
    def validate_method(cls, value: str) -> str:
        """验证并标准化HTTP方法"""
        valid_methods = {
            "GET", "POST", "PUT", "DELETE", 
            "PATCH", "HEAD", "OPTIONS", "CONNECT", "TRACE"
        }
        standardized = value.upper()
        if standardized not in valid_methods:
            raise ValueError(f"不支持的HTTP方法: {value}")
        return standardized

    @field_validator('url')
    def validate_url(cls, value: str) -> str:
        """验证URL格式有效性"""
        if not validators.url(value):
            raise ValueError(f"无效的URL格式: {value}")
        return value

    @field_validator('data', 'json_data')
    def check_data_conflict(cls, value, values):
        """确保data和json_data不同时存在"""
        if 'data' in values and 'json_data' in values:
            if values['data'] is not None and values['json_data'] is not None:
                raise ValueError("data和json_data不能同时存在")
        return value