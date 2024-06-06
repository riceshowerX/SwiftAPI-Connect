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
    **kwargs: Dict[str, Any]
) -> httpx.Response:
    async with httpx.AsyncClient(timeout=timeout) as client:
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
            logging.debug(f"Request headers: {response.request.headers}")
            logging.debug(f"Request body: {response.request.content}")
            logging.debug(f"Response headers: {response.headers}")
            logging.debug(f"Response body: {response.text}")
            logging.info(f"Received response: {response.status_code}")

            response.raise_for_status() 
            return response

        except httpx.HTTPStatusError as exc:
            logging.error(f"HTTP error occurred while requesting {exc.request.url!r}: {exc}")
            raise HTTPError(status_code=exc.response.status_code, detail=exc.response.text)

        except httpx.RequestError as exc:
            logging.error(f"An error occurred while requesting {exc.request.url!r}: {exc}")
            raise HTTPError(status_code=500, detail=str(exc))

        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            raise HTTPError(status_code=500, detail=str(e))