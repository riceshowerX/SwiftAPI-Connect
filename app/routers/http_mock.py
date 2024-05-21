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

@router.post("/request", response_model=HTTPResponseSchema)
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

        response_data = HTTPResponseSchema(
            status_code=response.status_code,
            text=response.text,
            headers=dict(response.headers),
            elapsed=response.elapsed.total_seconds(),
            encoding=response.encoding,  # 添加 encoding 信息
            content_type=response.headers.get("Content-Type"),  # 添加 content_type 信息
        )
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