#  request_helper.py
import httpx
import logging

async def send_http_request(method, url, **kwargs):
    async with httpx.AsyncClient(timeout=30.0) as client:  # 设置超时时间为30秒
        try:
            logging.info(f"Sending {method} request to {url} with params: {kwargs}")
            response = await client.request(method=method, url=url, **kwargs)
            logging.info(f"Received response: {response.status_code}")
            return response
        except httpx.RequestError as exc:
            logging.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise
