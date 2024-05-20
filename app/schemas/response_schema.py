# response_schema.py
from typing import Dict

from pydantic import BaseModel

class HTTPResponseSchema(BaseModel):
    status_code: int
    text: str
    headers: Dict[str, str]
    elapsed: float