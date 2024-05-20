# http_mock.py
from fastapi import APIRouter, HTTPException, Request
from app.utils.request_helper import send_http_request
from app.schemas.request_schema import HTTPRequestSchema
from app.schemas.response_schema import HTTPResponseSchema

router = APIRouter(
    prefix="/mock",
    tags=["HTTP Mock"]
)

@router.post("/request", response_model=HTTPResponseSchema)
async def make_request(request: Request, data: HTTPRequestSchema):
    try:
        response = await send_http_request(
            method=data.method,
            url=data.url,
            params=data.params,
            headers=data.headers,
            data=data.data,
            json=data.json_data,  # 修改后的字段名
            encoding=data.encoding,
        )

        return {
            "status_code": response.status_code,
            "text": response.text,
            "headers": dict(response.headers),
            "elapsed": response.elapsed.total_seconds()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))