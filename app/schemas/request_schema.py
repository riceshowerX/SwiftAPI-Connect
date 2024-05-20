# request_schema.py
from typing import Dict, Optional, Union

from pydantic import BaseModel, AnyUrl

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
    method: str
    url: AnyUrl
    params: Optional[Dict[str, str]] = {}
    headers: Optional[Dict[str, str]] = {}
    data: Optional[Union[str, Dict]] = None
    json_data: Optional[Dict] = None
    encoding: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if v.params is None:
            v.params = {}
        if v.headers is None:
            v.headers = {}
        return v
