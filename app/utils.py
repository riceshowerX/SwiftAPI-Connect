# utils.py
import logging
import re
from urllib.parse import urlparse
from typing import Optional

logger = logging.getLogger(__name__)

ALLOWED_SCHEMES = ['http', 'https']
FORBIDDEN_DOMAINS = ['example.com', 'test.com']


def validate_url(url: str, allowed_schemes: Optional[list] = None, forbidden_domains: Optional[list] = None) -> bool:
    """
    验证 URL 的有效性

    参数:
    url (str): 要验证的 URL
    allowed_schemes (list, optional): 允许的协议schemes列表,默认为['http', 'https']
    forbidden_domains (list, optional): 禁止的域名列表,默认为['example.com', 'test.com']

    返回值:
    bool: 如果 URL 有效,则返回 True,否则返回 False
    """
    allowed_schemes = allowed_schemes or ALLOWED_SCHEMES
    forbidden_domains = forbidden_domains or FORBIDDEN_DOMAINS

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc

    # 检查协议是否允许
    if scheme not in allowed_schemes:
        logger.warning(f"URL {url} has an unsupported scheme: {scheme}")
        return False

    # 检查域名是否禁止
    if any(domain in netloc for domain in forbidden_domains):
        logger.warning(f"URL {url} contains a forbidden domain: {netloc}")
        return False

    # 检查URL格式是否合法
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not url_regex.match(url):
        logger.warning(f"URL {url} is not a valid URL format")
        return False

    logger.info(f"URL {url} is valid")
    return True