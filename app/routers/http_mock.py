# http_mock.py
from fastapi import APIRouter, HTTPException, Request
from app.utils.request_helper import send_http_request
from app.schemas.request_schema import HTTPRequestSchema
from app.schemas.response_schema import HTTPResponseSchema
from fastapi.responses import JSONResponse
from app.errors.http_errors import HTTPError
from app.utils.crypto import decrypt_data
from fastapi_server import ENCRYPTION_KEY
import logging
import json

router = APIRouter(
    prefix="/mock",
    tags=["HTTP Mock"]
)

@router.post("/request", response_model=HTTPResponseSchema, response_model_exclude_none=True)
async def make_request(request: Request, data: HTTPRequestSchema):
    logging.info(f"Received request: {data.json()}")
    try:
        # 解密请求数据
        if data.data:
            data.data = decrypt_data(data.data.encode(), ENCRYPTION_KEY).decode()
        if data.json_data:
            data.json_data = json.loads(decrypt_data(json.dumps(data.json_data).encode(), ENCRYPTION_KEY).decode())

        response = await send_http_request(
            method=data.method,
            url=data.url,
            params=data.params,
            headers=data.headers,
            data=data.data,
            json=data.json_data,  # 使用 'json' 参数
            encoding=data.encoding,
        )

        response_data = HTTPResponseSchema.from_attributes(response)  # 使用 from_attributes 方法初始化
        logging.info(f"Returning response: {response_data.json()}")
        return JSONResponse(response_data.to_dict())  # 使用 to_dict 方法序列化

    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))