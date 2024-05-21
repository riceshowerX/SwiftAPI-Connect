# http_mock.py
from fastapi import APIRouter, HTTPException, Request
from app.utils.request_helper import send_http_request
from app.schemas.request_schema import HTTPRequestSchema
from app.schemas.response_schema import HTTPResponseSchema
from fastapi.responses import JSONResponse
import logging

router = APIRouter(
    prefix="/mock",
    tags=["HTTP Mock"]
)

@router.post("/request", response_model=HTTPResponseSchema, response_model_exclude_none=True)  # 添加 response_model_exclude_none=True
async def make_request(request: Request, data: HTTPRequestSchema):
    logging.info(f"Received request: {data}")
    try:
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
        logging.info(f"Returning response: {response_data}")
        return JSONResponse(response_data.to_dict())  # 使用 to_dict 方法序列化
    except TimeoutError as e:
        logging.error(f"TimeoutError: {e}")
        raise HTTPException(status_code=504, detail="Gateway Timeout")
    except ConnectionError as e:
        logging.error(f"ConnectionError: {e}")
        raise HTTPException(status_code=502, detail="Bad Gateway")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))