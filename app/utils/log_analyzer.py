# app/utils/log_analyzer.py
import logging
import re
from collections import defaultdict

# 初始化日志记录器
logging.basicConfig(level=logging.INFO)

def analyze_logs(log_file: str) -> Dict[str, int]:
    """
    分析日志文件，统计请求方法和状态码

    Args:
        log_file: 日志文件路径

    Returns:
        字典，包含请求方法和状态码的统计结果
    """
    request_counts = defaultdict(int)
    status_code_counts = defaultdict(int)

    with open(log_file, 'r') as f:
        for line in f:
            # 使用正则表达式提取请求方法和状态码
            match = re.search(r'Request: (\w+) (.*?)\s+Response: (\d+)', line)
            if match:
                method = match.group(1)
                status_code = match.group(3)
                request_counts[method] += 1
                status_code_counts[status_code] += 1

    logging.info(f"Request Counts: {request_counts}")
    logging.info(f"Status Code Counts: {status_code_counts}")

    return {
        'request_counts': request_counts,
        'status_code_counts': status_code_counts
    }