# app.py
import streamlit as st
import requests
import json
import logging
import time
import chardet

from typing import Dict, Optional, Union
from pydantic import BaseModel, AnyUrl, Field, field_validator

from ui.components.request_form import get_params 
from ui.components.progress_bar import show_progress_bar

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components.request_form import get_params

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
    data: Optional[Union[str, Dict]] = Field(None, description="请求体数据")
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


def send_request(method, url, params, headers, data, json_data, encoding):
    try:
        # 使用进度条组件
        show_progress_bar()
        
        response = requests.request(
            method, url, params=params, headers=headers, data=data, json=json_data
        )

        return response
    except Exception as e:
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

        except Exception as e:
            st.error(f"请求失败: {str(e)}")


if __name__ == "__main__":
    run_ui()