#  request_helper.py
import httpx
import logging
from typing import Dict, Any, Optional

async def send_http_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    json: Optional[Any] = None,
    **kwargs: Dict[str, Any]
):
    """
    发送 HTTP 请求

    Args:
        method: HTTP 请求方法，例如 'GET', 'POST', 'PUT', 'DELETE'
        url: 请求 URL
        headers: 请求头
        params: 请求参数
        data: 请求体（表单数据）
        json: 请求体（JSON 数据）
        **kwargs: 其他请求参数

    Returns:
        httpx.Response: HTTP 响应对象

    Raises:
        httpx.RequestError: HTTP 请求错误
        Exception: 其他错误
    """

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            logging.info(f"Sending {method} request to {url} with params: {kwargs}")
            response = await client.request(
                method=method, 
                url=url, 
                headers=headers, 
                params=params, 
                data=data, 
                json=json,
                **kwargs
            )
            logging.debug(f"Received response: {response.status_code}")
            logging.debug(f"Request headers: {response.request.headers}")
            logging.debug(f"Request body: {response.request.content}")
            logging.debug(f"Response headers: {response.headers}")
            logging.debug(f"Response body: {response.text}")
            return response
        except httpx.RequestError as exc:
            logging.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise