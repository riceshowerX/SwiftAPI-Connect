# scraper.py
import aiohttp
import logging
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlencode

logger = logging.getLogger(__name__)

default_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299",
    "Accept": "*/*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}

async def prepare_request_data(method, data, url):
    if method.upper() == 'GET' and data:
        return url + '?' + urlencode(data), None
    elif method.upper() == 'POST':
        default_headers['Content-Type'] = 'application/json'
        return url, json.dumps(data) if isinstance(data, dict) else None
    return url, None

async def scrape_website_async(url, method='GET', data=None, headers=None, cookies=None, proxy=None, max_redirects=5):
    if not urlparse(url).netloc:
        raise ValueError("Invalid URL. Missing network location.")

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
