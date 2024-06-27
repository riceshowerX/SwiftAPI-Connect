# http_mock.py
from fastapi import APIRouter, HTTPException, Request, Depends, status
from fastapi.responses import JSONResponse
import logging
import uuid

from app.core.utils.request_helper import send_http_request
from app.core.schemas.request_schema import HTTPRequestSchema
from app.core.schemas.response_schema import HTTPResponseSchema
from app.core.errors.http_errors import HTTPError
from app.core.utils.crypto import encrypt_data, decrypt_data
from app.core.config import settings

router = APIRouter(
    prefix="/mock",
    tags=["HTTP Mock"]
)

async def get_encryption_status(request: Request) -> bool:
    return request.headers.get("Encryption", "False").lower() == "true"

def encrypt_request_data(data: HTTPRequestSchema):
    data.url = encrypt_data(data.url)
    if data.params is not None:
        data.params = {k: encrypt_data(v) for k, v in data.params.items()}
    if data.headers is not None:
        data.headers = {k: encrypt_data(v) for k, v in data.headers.items()}
    if data.data is not None:
        data.data = encrypt_data(data.data)
    if data.json_data is not None:
        data.json_data = {k: encrypt_data(v) for k, v in data.json_data.items()}
    return data

def decrypt_response_data(response_data: HTTPResponseSchema):
    response_data.text = decrypt_data(response_data.text)
    response_data.headers = {k: decrypt_data(v) for k, v in response_data.headers.items()}
    return response_data

@router.post("/request", response_model=HTTPResponseSchema, response_model_exclude_none=True)
async def make_request(request: Request, data: HTTPRequestSchema, encryption_enabled: bool = Depends(get_encryption_status)):
    request_id = str(uuid.uuid4())
    logging.info(f"Request ID {request_id} - Received request: {data}")
    try:
        if encryption_enabled:
            data = encrypt_request_data(data)

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
            response_data = decrypt_response_data(response_data)

        logging.info(f"Request ID {request_id} - Returning response: {response_data}")
        return JSONResponse(response_data.to_dict())

    except HTTPError as e:
        logging.error(f"Request ID {request_id} - HTTP error: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail=e.detail)

    except ValueError as e:
        logging.error(f"Request ID {request_id} - Value error: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except Exception as e:
        logging.error(f"Request ID {request_id} - Unexpected error: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))