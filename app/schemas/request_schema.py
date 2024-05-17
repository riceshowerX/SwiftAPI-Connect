from typing import Dict, Optional, Union

from pydantic import BaseModel, HttpUrl

class HTTPRequestSchema(BaseModel):
    method: str
    url: HttpUrl
    params: Optional[Dict[str, str]] = None
    headers: Optional[Dict[str, str]] = None
    data: Optional[Union[str, Dict]] = None
    json_data: Optional[Dict] = None  # 修改后的字段名
    encoding: Optional[str] = None