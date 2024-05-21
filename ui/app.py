# app.py
import streamlit as st
import requests
import json
import logging
import time
import chardet
import sys
sys.path.insert(0, 'C:\\Users\\21440\\Documents\\GitHub\\SwiftAPI-Connect')
from app.utils.crypto import encrypt_data




from typing import Dict, Optional, Union
from pydantic import BaseModel, AnyUrl, Field, field_validator
from requests.exceptions import RequestException

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

# 复制 COMMON_ENCODINGS 变量
COMMON_ENCODINGS = [
    "ascii",
    "utf-8",
    "utf-16",
    "utf-32",
    "latin-1",
    "gbk",
    "gb18030",
    "big5",
    "shift-jis",
    "euc-jp",
    "euc-kr",
]

# 从环境变量获取加密密钥
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")

class HTTPRequestSchema(BaseModel):
    """
    HTTP 请求模式定义
    """

    method: str = Field(..., description="HTTP 方法", example="GET")
    url: AnyUrl = Field(..., description="请求 URL", example="https://example.com")
    params: Optional[Dict[str, str]] = Field(
        {}, description="查询参数", example={"key1": "value1", "key2": "value2"}
    )
    headers: Optional[Dict[str, str]] = Field(
        {}, description="请求头", example={"User-Agent": "Mozilla/5.0"}
    )
    data: Optional[str] = Field(None, description="请求体数据")
    json_data: Optional[Dict] = Field(None, description="JSON 请求体数据")
    encoding: Optional[str] = Field(
        None, description="请求体的编码", example="utf-8"
    )

    @field_validator("method")
    def method_must_be_valid(cls, value):
        valid_methods = [
            "GET",
            "POST",
            "PUT",
            "DELETE",
            "PATCH",
            "HEAD",
            "OPTIONS",
            "CONNECT",
            "TRACE",
        ]
        if value.upper() not in valid_methods:
            raise ValueError(
                f"Invalid HTTP method: {value}. Valid methods are: {valid_methods}"
            )
        return value.upper()  # 统一转换为大写


def get_params(param_type, key_prefix, value_prefix):
    params = {}
    with st.expander(f"{param_type} 参数"):
        param_count = st.number_input(
            f"{param_type} 参数数量", min_value=0, step=1, key=f"{param_type}_params_count"
        )
        for i in range(param_count):
            col1, col2 = st.columns(2)
            with col1:
                key = st.text_input(
                    f"{param_type} 参数 {i+1} 的 Key", key=f"{key_prefix}_{i}"
                )
            with col2:
                value = st.text_input(
                    f"{param_type} 参数 {i+1} 的 Value", key=f"{value_prefix}_{i}"
                )
            params[key] = value
    return params


def send_request(method, url, params, headers, data, json_data, encoding):
    try:
        # 创建进度条
        progress_bar = st.progress(0)

        # 模拟请求处理时间
        for i in range(10):
            time.sleep(0.1)
            progress_bar.progress(i * 10)

        # 加密请求数据
        if data:
            data = encrypt_data(data.encode(), ENCRYPTION_KEY).decode()
        if json_data:
            json_data = json.loads(encrypt_data(json.dumps(json_data).encode(), ENCRYPTION_KEY).decode())

        response = requests.request(
            method, url, params=params, headers=headers, data=data, json=json_data
        )

        # 设置进度条为 100%
        progress_bar.progress(100)

        return response
    except RequestException as e:
        logging.error(f"Request failed: {e}")
        raise

def update_api_key():
    """更新 API Key 到 session_state"""
    st.session_state.api_key = st.session_state.api_key_input

def run_ui():
    st.title("HTTP 请求模拟工具")

    # 选择 HTTP 方法
    method = st.selectbox(
        "选择 HTTP 方法",
        ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "TRACE"],
        key="method",
    )

    # 输入 URL
    url = st.text_input("输入 URL", key="url")

    # 参数输入区域
    st.header("参数")
    query_params = get_params("查询", "query_key", "query_value")
    form_params = get_params("表单", "form_key", "form_value")

    json_data = None
    with st.expander("JSON 参数"):
        json_str = st.text_area("输入 JSON 字符串", key="json_data")
        if json_str:
            try:
                json_data = json.loads(json_str)
            except json.JSONDecodeError:
                st.error("JSON 格式错误！")

    # Header 输入区域
    st.header("Header")
    headers = get_params("Header", "header_key", "header_value")

    # 使用secrets存储API Key
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    st.session_state.api_key_input = st.text_input(
        "输入 API Key", key="api_key", value=st.session_state.api_key, on_change=update_api_key
    )
    headers["x-api-key"] = st.session_state.api_key

    # Data 输入区域
    st.header("Data")
    data = st.text_area("输入 Data", key="data_info")

    # 编码选择
    encoding = st.selectbox("选择编码", COMMON_ENCODINGS, key="encoding")

    # 发送请求按钮
    if st.button("发送请求"):
        try:
            # 使用 Pydantic 模型验证请求参数
            request_data = HTTPRequestSchema(
                method=method,
                url=url,
                params=query_params,
                headers=headers,
                data=data,
                json_data=json_data,
                encoding=encoding,
            )
            logging.info(f"Request data: {request_data}")

            response = send_request(
                method=request_data.method,
                url=request_data.url,
                params=request_data.params,
                headers=request_data.headers,
                data=request_data.data,
                json_data=request_data.json_data,
                encoding=request_data.encoding,
            )

            # 自动检测响应编码
            detected_encoding = chardet.detect(response.content)["encoding"]
            logging.info(f"Detected response encoding: {detected_encoding}")
            response_text = response.content.decode(
                detected_encoding, errors="replace"
            )

            # 展示结果
            st.header("请求结果")
            st.write(f"状态码: {response.status_code}")
            st.write(f"响应时间: {response.elapsed.total_seconds()} 秒")
            st.write("响应 Header:")
            st.json(dict(response.headers))
            st.write("响应内容:")
            st.text(response_text)

        except RequestException as e:
            st.error(f"请求失败: {str(e)}")
        except ValueError as e:
            st.error(f"验证失败: {str(e)}")


if __name__ == "__main__":
    run_ui()