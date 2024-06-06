# http_mock.py
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse

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

async def get_encryption_status(request: Request) -> bool:
    return request.headers.get("Encryption", "False").lower() == "true"

@router.post("/request", response_model=HTTPResponseSchema, response_model_exclude_none=True)
async def make_request(request: Request, data: HTTPRequestSchema, encryption_enabled: bool = Depends(get_encryption_status)):
    logging.info(f"Received request: {data}")
    try:
        if encryption_enabled:
            data.url = encrypt_data(data.url)
            if data.params is not None:
                data.params = {k: encrypt_data(v) for k, v in data.params.items()}
            if data.headers is not None:
                data.headers = {k: encrypt_data(v) for k, v in data.headers.items()}
            if data.data is not None:
                data.data = encrypt_data(data.data)
            if data.json_data is not None:
                data.json_data = {k: encrypt_data(v) for k, v in data.json_data.items()}

        response = await send_http_request(
            method=data.method,
            url=data.url,
            params=data.params,
            headers=data.headers,
            data=data.data,
            json=data.json_data,  
            encoding=data.encoding,
        )

        response_data = HTTPResponseSchema.from_attributes(response)

        if encryption_enabled:
            response_data.text = decrypt_data(response_data.text)
            response_data.headers = {k: decrypt_data(v) for k, v in response_data.headers.items()}

        logging.info(f"Returning response: {response_data}")
        return JSONResponse(response_data.to_dict())

    except HTTPError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=str(e))