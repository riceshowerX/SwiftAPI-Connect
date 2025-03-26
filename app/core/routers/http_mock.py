from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from typing import Dict, Optional

from app.core.utils.request_helper import send_http_request
from app.core.schemas.request_schema import HTTPRequestSchema
from app.core.schemas.response_schema import HTTPResponseSchema
from app.core.errors.http_errors import HTTPError
from app.core.utils.crypto import encrypt_data, decrypt_data
import logging

router = APIRouter(
    prefix="/mock",
    tags=["HTTP Mock"]
)

def get_encryption_status(request: Request) -> bool:
    """提取加密状态的依赖函数"""
    return request.headers.get("Encryption", "False").lower() == "true"

def process_encryption(data: Dict, encrypt_func: callable) -> Dict:
    """递归处理加密/解密的通用函数"""
    processed = {}
    for k, v in data.items():
        if isinstance(v, dict):
            processed[k] = process_encryption(v, encrypt_func)
        else:
            processed[k] = encrypt_func(v) if v is not None else v
    return processed

@router.post("/request", response_model=HTTPResponseSchema)
async def make_request(
    request: Request,
    data: HTTPRequestSchema,
    encryption_enabled: bool = Depends(get_encryption_status)
):
    """处理HTTP请求的模拟端点"""
    logging.info(f"Received {data.method} request to {data.url}")
    
    try:
        # 加密处理
        if encryption_enabled:
            data_dict = data.model_dump(exclude_unset=True)
            encrypted_data = process_encryption(data_dict, encrypt_data)
            data = HTTPRequestSchema(**encrypted_data)

        # 发送请求
        response = await send_http_request(**data.model_dump(exclude_unset=True))
        response_data = HTTPResponseSchema.from_attributes(response)

        # 解密处理
        if encryption_enabled:
            response_dict = response_data.model_dump(exclude_unset=True)
            decrypted_data = process_encryption(response_dict, decrypt_data)
            response_data = HTTPResponseSchema(**decrypted_data)

        return JSONResponse(response_data.model_dump(exclude_unset=True))

    except HTTPError as e:
        logging.error(f"HTTP error occurred: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    except Exception as e:
        logging.exception("Unexpected error occurred")
        raise HTTPException(status_code=500, detail="Internal server error")