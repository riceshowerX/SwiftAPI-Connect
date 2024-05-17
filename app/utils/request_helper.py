import httpx

async def send_http_request(method, url, **kwargs):
    async with httpx.AsyncClient() as client:
        response = await client.request(method=method, url=url, **kwargs)
        return response