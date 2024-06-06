# main_ui.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.components.request_form import get_params
from ui.components.progress_bar import show_progress_bar

import streamlit as st
import requests
import json
import logging
import time
import chardet
import asyncio

from typing import Dict, Optional, Union
from pydantic import BaseModel, AnyUrl, Field, field_validator
from cryptography.fernet import Fernet

from app.core.services.mock_data_service import MockDataService
from app.core.services.task_scheduler import TaskScheduler

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


def send_request(method, url, params, headers, data, json_data, encoding, encryption_enabled):
    try:
        # 使用进度条组件
        show_progress_bar()

        # 添加加密头信息
        if encryption_enabled:
            headers["Encryption"] = "True"
        else:
            headers["Encryption"] = "False"

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


def generate_encryption_key():
    """生成新的加密密钥并保存到 session_state"""
    key = Fernet.generate_key()
    st.session_state.encryption_key = key.decode()
    st.success("新的加密密钥已生成！")

# 初始化服务
mock_data_service = MockDataService()
task_scheduler = TaskScheduler()


def run_ui():
    st.title("HTTP 请求模拟工具")

    # --- Mock 数据管理 ---
    st.header("Mock 数据管理")
    with st.expander("创建 Mock 数据"):
        key = st.text_input("Key", key="mock_data_key")
        data = st.text_area("Data (JSON 格式)", key="mock_data_value")
        if st.button("创建", key="create_mock_data"):
            try:
                mock_data_service.create_mock_data(key, json.loads(data))
                st.success("Mock 数据创建成功!")
            except json.JSONDecodeError:
                st.error("数据格式错误，请检查 JSON 格式!")

    with st.expander("获取 Mock 数据"):
        key = st.text_input("Key", key="get_mock_data_key")
        if st.button("获取", key="get_mock_data"):
            data = mock_data_service.get_mock_data(key)
            if data:
                st.json(data)
            else:
                st.warning("找不到该 Key 对应的 Mock 数据")

    # --- 其他 Mock 数据管理功能，例如更新和删除 ---

    # --- 任务调度 ---
    st.header("任务调度")
    with st.expander("添加定时任务"):
        url = st.text_input("请求 URL", key="task_url")
        interval = st.number_input("间隔时间 (秒)", min_value=1, key="task_interval")
        if st.button("添加任务", key="add_task"):
            async def send_request_task():
                while True:
                    try:
                        response = requests.get(url)
                        logging.info(f"定时任务执行成功，状态码: {response.status_code}")
                    except Exception as e:
                        logging.error(f"定时任务执行失败: {e}")
                    await asyncio.sleep(interval)
            task_scheduler.add_task(send_request_task())
            st.success("定时任务已添加")

    if st.button("启动任务调度器"):
        asyncio.run(task_scheduler.run_tasks())

    # --- HTTP 请求模拟工具 ---
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

    # 使用 secrets 存储 API Key
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

    # 加密选项区域
    st.header("加密选项")
    encryption_enabled = st.checkbox("开启加密", key="encryption_enabled")

    # 自动生成密钥按钮
    if st.button("生成新的加密密钥"):
        generate_encryption_key()

    # 显示加密密钥
    if "encryption_key" in st.session_state:
        st.write("**加密密钥:**", st.session_state.encryption_key)
        st.info("请妥善保管此密钥，不要将其分享给他人！")

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
                encryption_enabled=encryption_enabled,
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