#  network_utils.py
import httpx
import logging
from typing import Dict, Any, Optional
from app.core.errors.http_errors import HTTPError
from app.core.utils.crypto_utils import encrypt_data, decrypt_data

async def send_http_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    json: Optional[Any] = None,
    timeout: Optional[float] = None,
    encryption_enabled=False,
    **kwargs: Dict[str, Any]
) -> httpx.Response:
    """
    发送 HTTP 请求

    Args:
        method: HTTP 请求方法，例如 'GET', 'POST', 'PUT', 'DELETE'
        url: 请求 URL
        headers: 请求头
        params: 请求参数
        data: 请求体（表单数据）
        json: 请求体（JSON 数据）
        timeout: 请求超时时间 (秒)
        **kwargs: 其他请求参数

    Returns:
        httpx.Response: HTTP 响应对象

    Raises:
        HTTPError: HTTP 请求错误
    """

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            logging.info(f"Sending {method} request to {url}")
            if encryption_enabled:
                data = encrypt_data(data.encode()) if isinstance(data, str) else data
                json = encrypt_data(json.encode()) if isinstance(json, str) else json
            response = await client.request(
                method=method, 
                url=url, 
                headers=headers, 
                params=params, 
                data=data, 
                json=json,
                **kwargs
            )
            logging.debug(f"Request headers: {response.request.headers}")
            logging.debug(f"Request body: {response.request.content}")
            logging.debug(f"Response headers: {response.headers}")
            logging.debug(f"Response body: {response.text}")
            logging.info(f"Received response: {response.status_code}")

            response.raise_for_status()  # 如果状态码 >= 400 则抛出异常
            return response

        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error occurred while requesting {exc.request.url!r}: {exc}")
            raise HTTPError(status_code=exc.response.status_code, detail=exc.response.text) from exc

        except httpx.RequestError as exc:
            logging.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise HTTPError(status_code=500, detail=str(exc)) from exc

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise HTTPError(status_code=500, detail=str(e)) from e