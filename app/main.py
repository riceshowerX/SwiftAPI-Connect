# app/main.py
from fastapi import FastAPI, HTTPException, Request
from app.utils.request_helper import send_http_request
from app.schemas.request_schema import HTTPRequestSchema
from app.schemas.response_schema import HTTPResponseSchema
from fastapi.responses import JSONResponse
from app.security.encryption_helper import encrypt_request, decrypt_request
import logging

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="HTTP Mock Server",
    description="A simple HTTP mock server built with FastAPI",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],
)

router = APIRouter(
    prefix="/mock",
    tags=["HTTP Mock"]
)

@router.post("/request", response_model=HTTPResponseSchema)
async def make_request(request: Request, data: HTTPRequestSchema):
    try:
        # 加密请求数据
        encrypted_data = encrypt_request(data.data) if data.data else data.data
        
        response = await send_http_request(
            method=data.method,
            url=data.url,
            params=data.params,
            headers=data.headers,
            data=encrypted_data,
            json_data=data.json_data,
            encoding=data.encoding,
        )

        response_data = {
            "status_code": response.status_code,
            "text": response.text,
            "headers": dict(response.headers),
            "elapsed": response.elapsed.total_seconds()
        }

        return JSONResponse(response_data)
    except TimeoutError as e:
        raise HTTPException(status_code=504, detail="Gateway Timeout")
    except ConnectionError as e:
        raise HTTPException(status_code=502, detail="Bad Gateway")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(router)

logging.info("FastAPI application setup complete.")