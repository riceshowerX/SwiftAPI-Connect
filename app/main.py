# main.py
import asyncio
import time
from functools import wraps
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse
from app.scraper import scrape_website_async
from fastapi.staticfiles import StaticFiles
from app.scraper import scrape_website_async
from app.utils import validate_url
from app.encryption import encrypt_data
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlencode
import aiohttp
import logging
import json

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/templates/static"), name="static")

# 设置日志记录器
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def retry_request(retries=3, delay=1):
    """
    请求重试装饰器，最多重试retries次，间隔delay秒。
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    logger.warning(f"请求失败，正在重试... {e}")
                    await asyncio.sleep(delay)
            raise HTTPException(status_code=500, detail="请求失败，已达最大重试次数")
        return wrapper
    return decorator

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"发生了错误: {exc}")
    # 记录请求信息
    logger.error(f"URL: {request.url}")
    logger.error(f"方法: {request.method}")
    raise HTTPException(status_code=500, detail="内部服务器错误")

@app.get("/", response_class=HTMLResponse)
async def read_item():
    with open("app/templates/index.html", "r", encoding="utf-8") as file:
        content = file.read()
    return content

async def prepare_request_data(method, data, url):
    if method.upper() == 'GET' and data:
        return url + '?' + urlencode(data), None
    elif method.upper() == 'POST':
        return url, json.dumps(data) if isinstance(data, dict) else None
    return url, None

async def scrape_website_async(url, method='GET', data=None, headers=None, cookies=None, proxy=None, max_redirects=5):
    if not urlparse(url).netloc:
        raise ValueError("Invalid URL. Missing network location.")

    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }

    if headers:
        default_headers.update(headers)

    async with aiohttp.ClientSession(cookies=cookies) as session:
        redirect_count = 0
        while redirect_count < max_redirects:
            url, data = await prepare_request_data(method, data, url)
            try:
                async with session.request(method, url, headers=default_headers, data=data, allow_redirects=False, proxy=proxy) as response:
                    if response.status == 200:
                        soup = BeautifulSoup(await response.text(), 'html.parser')
                        titles = [title.text for title in soup.find_all('h1')]
                        logger.info(f"Request to {url} successful. Titles: {titles}")
                        return titles
                    elif response.status == 307:
                        location = response.headers.get('Location')
                        if not urlparse(location).netloc:
                            raise ValueError("Invalid redirect location.")
                        logger.info(f"Redirecting to: {location}")
                        url = location
                        redirect_count += 1
                    else:
                        logger.error(f"Failed to fetch data from {url}. Status code: {response.status}")
                        raise ValueError(f"Failed to fetch data from the website. Status code: {response.status}")
            except Exception as e:
                logger.error(f"Error during request to {url}: {e}")
                raise

        raise ValueError(f"Exceeded maximum redirects ({max_redirects})")

@app.post("/request/")
@app.get("/request/")
@retry_request()
async def send_request(url: str = Query(..., description="要发送请求的网站的URL"),
                       method: str = Query("GET", description="请求方法（GET、POST、PUT、DELETE、HEAD、TRACE、OPTIONS、PATCH 等）"),
                       data: str = Query(None, description="可选的要与请求一起发送的数据"),
                       encoding: str = Query("UTF-8", description="编码格式（UTF-8、GBK、GB2312、GB18030）"),
                       custom_headers: str = Query(None, description="自定义 Header(JSON格式)"),
                       cookie: str = Query(None, description="Cookie"),
                       proxy: str = Query(None, description="IP代理地址")):
    if not validate_url(url):
        raise HTTPException(status_code=400, detail="URL 格式无效或不允许该域名。")
    try:
        data_dict = None
        if data:
            try:
                data_dict = json.loads(data)
            except json.JSONDecodeError:
                pass
        headers = {
            "Content-Type": "application/json"
        }
        if custom_headers:
            try:
                custom_headers_dict = json.loads(custom_headers)
                headers.update(custom_headers_dict)
            except json.JSONDecodeError:
                pass
        if cookie:
            headers["Cookie"] = cookie
        # 在发送请求之前对数据进行加密
        encrypted_data = None
        if data_dict:
            iv, encrypted_data = encrypt_data(json.dumps(data_dict))
            data = json.dumps({"iv": iv, "data": encrypted_data})
        if proxy:
            headers["Proxy"] = proxy
        result = await scrape_website_async(url, method=method, data=data, headers=headers)
        return {"success": True, "result": result}
    except aiohttp.ClientError as e:
        logger.error(f"发送请求时发生错误: {e}")
        # 记录请求信息
        logger.error(f"URL: {url}")
        logger.error(f"方法: {method}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate-request/")
async def simulate_request(request: Request):
    method = request.method
    url = str(request.url)
    headers = dict(request.headers)
    params = await request.body()

    # 记录请求信息
    logger.info(f"方法: {method}")
    logger.info(f"URL: {url}")
    logger.info(f"头部: {headers}")
    logger.info(f"参数: {params.decode('utf-8')}")

    return {
        "success": True,
        "message": "请求模拟成功",
        "method": method,
        "url": url,
        "headers": headers,
        "parameters": params.decode('utf-8')
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
