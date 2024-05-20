# response_schema.py
from typing import Dict, Optional, Union, List

from pydantic import BaseModel, Field

class HTTPResponseSchema(BaseModel):
    """
    HTTP 响应模式定义

    :param status_code: 响应状态码
    :param text: 响应正文内容
    :param headers: 响应头信息
    :param elapsed: 响应时间（秒）
    """

    status_code: int = Field(..., description="响应状态码", example=200)
    text: Optional[Union[str, bytes]] = Field(None, description="响应正文内容")
    headers: Dict[str, Union[str, List[str]]] = Field(..., description="响应头信息")
    elapsed: float = Field(..., description="响应时间（秒）", example=0.5)