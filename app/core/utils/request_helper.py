import httpx
import asyncio
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
    timeout: Optional[float] = 5.0,
    retries: int = 3,
    backoff_factor: float = 0.3,
    encoding: Optional[str] = None,
    **kwargs: Dict[str, Any]
) -> httpx.Response:
    """
    增强型异步HTTP请求发送函数
    
    Args:
        method: HTTP方法（GET/POST等）
        url: 请求URL
        headers: 请求头
        params: URL查询参数
        data: 表单数据
        json: JSON请求体数据
        timeout: 超时时间（秒）
        retries: 最大重试次数
        backoff_factor: 重试间隔因子
        encoding: 响应编码
        **kwargs: 其他httpx参数
        
    Returns:
        httpx.Response 对象
        
    Raises:
        HTTPError: 请求失败时抛出
    """
    validate_request_body(data, json)
    
    async def attempt_request() -> httpx.Response:
        """执行单次请求尝试"""
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                **kwargs
            )
            response.raise_for_status()
            return response
            
    for attempt in range(retries + 1):
        try:
            response = await attempt_request()
            configure_response_encoding(response, encoding)
            log_request_details(response, attempt, retries)
            return response
            
        except httpx.HTTPStatusError as e:
            handle_http_error(e, attempt, retries, backoff_factor)
        except httpx.RequestError as e:
            handle_request_error(e, attempt, retries, backoff_factor)
        except Exception as e:
            logging.exception("Unexpected error occurred")
            raise HTTPError(500, f"请求失败: {str(e)}")

def validate_request_body(data: Any, json_data: Any) -> None:
    """验证请求体参数冲突"""
    if data is not None and json_data is not None:
        raise ValueError("data和json参数不能同时使用")

def configure_response_encoding(response: httpx.Response, encoding: Optional[str]) -> None:
    """配置响应编码方式"""
    if encoding:
        response.encoding = encoding

def log_request_details(response: httpx.Response, attempt: int, max_retries: int) -> None:
    """记录请求详细信息"""
    logging.info(
        f"请求成功: {response.request.method} {response.url} "
        f"(尝试次数: {attempt+1}/{max_retries+1}), "
        f"状态码: {response.status_code}, "
        f"编码: {response.encoding}"
    )
    logging.debug(f"请求头: {response.request.headers}")
    logging.debug(f"响应头: {response.headers}")
    logging.debug(f"响应内容: {response.text}")

def handle_http_error(exc: httpx.HTTPStatusError, attempt: int, max_retries: int, backoff: float) -> None:
    """处理HTTP状态错误"""
    if attempt < max_retries:
        delay = backoff * (2 ** attempt)
        logging.warning(f"HTTP错误 {exc.response.status_code}, {delay:.1f}秒后重试...")
        asyncio.sleep(delay)
    else:
        raise HTTPError(exc.response.status_code, exc.response.text)

def handle_request_error(exc: httpx.RequestError, attempt: int, max_retries: int, backoff: float) -> None:
    """处理请求层错误"""
    if attempt < max_retries:
        delay = backoff * (2 ** attempt)
        logging.warning(f"请求错误: {str(exc)}, {delay:.1f}秒后重试...")
        asyncio.sleep(delay)
    else:
        raise HTTPError(500, str(exc))