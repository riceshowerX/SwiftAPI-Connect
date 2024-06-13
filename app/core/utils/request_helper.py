#  request_helper.py
import httpx
import logging
from typing import Dict, Any, Optional

from app.core.errors.http_errors import HTTPError

async def send_http_request(
    method: str,
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, str]] = None,
    data: Optional[Any] = None,
    json: Optional[Any] = None,
    timeout: Optional[float] = None,
    retries: int = 3,
    backoff_factor: float = 0.3, 
    **kwargs: Dict[str, Any]
) -> httpx.Response:
    """
    发送 HTTP 请求，并处理常见的异常情况。

    :param method: HTTP 请求方法，例如 GET、POST 等。
    :param url: 请求 URL。
    :param headers: 请求头信息，可选。
    :param params: URL 查询参数，可选。
    :param data: 请求体数据，可选。
    :param json: JSON 格式的请求体数据，可选。
    :param timeout: 请求超时时间，可选，单位为秒。
    :param retries: 最大重试次数。
    :param backoff_factor: 重试间隔的指数退避因子。
    :param kwargs: 其他关键字参数。
    :return: HTTP 响应对象。
    :raises HTTPError: 当 HTTP 请求失败时抛出。
    """
    for attempt in range(retries + 1):
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                logging.info(f"Sending {method} request to {url} (attempt {attempt + 1}/{retries + 1}) with params: {kwargs}")
                response = await client.request(
                    method=method,
                    url=url,
                    headers=headers,
                    params=params,
                    data=data,
                    json=json,
                    **kwargs,
                )
                logging.debug(f"Request headers: {response.request.headers}")
                logging.debug(f"Request body: {response.request.content}")
                logging.debug(f"Response headers: {response.headers}")
                logging.debug(f"Response body: {response.text}")
                logging.info(f"Received response: {response.status_code}")

                response.raise_for_status()  # 如果状态码不为 2xx，则抛出异常
                return response

        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error occurred while requesting {exc.request.url!r}: {exc}")
            if attempt < retries:
                # 计算重试间隔
                delay = backoff_factor * (2 ** attempt)
                logging.info(f"Retrying in {delay:.2f} seconds...")
                await asyncio.sleep(delay)
            else:
                raise HTTPError(status_code=exc.response.status_code, detail=exc.response.text)

        except httpx.RequestError as exc:
            logging.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            if attempt < retries:
                # 计算重试间隔
                delay = backoff_factor * (2 ** attempt)
                logging.info(f"Retrying in {delay:.2f} seconds...")
                await asyncio.sleep(delay)
            else:
                raise HTTPError(status_code=500, detail=str(exc))

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise HTTPError(status_code=500, detail=str(e))