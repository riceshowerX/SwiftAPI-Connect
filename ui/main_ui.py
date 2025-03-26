import sys
import os
import json
import logging
import time
import chardet
import asyncio
from typing import Dict, Optional, Union
import streamlit as st
import requests
from pydantic import BaseModel, AnyUrl, Field, field_validator, ValidationError
from cryptography.fernet import Fernet
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
import signal
from ui.components.request_form import get_params
from ui.components.progress_bar import show_progress_bar
from app.core.services.mock_data_service import MockDataService
from app.core.schemas.request_schema import HTTPRequestSchema
from app.core.schemas.response_schema import HTTPResponseSchema
from app.core.utils.request_helper import send_http_request, HTTPError
from app.core.utils.crypto import encrypt_data, decrypt_data

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

# 常见编码列表
COMMON_ENCODINGS = [
    "ascii", "utf-8", "utf-16", "utf-32", "latin-1",
    "gbk", "gb18030", "big5", "shift-jis", "euc-jp", "euc-kr"
]

class HTTPRequestSchema(BaseModel):
    """HTTP 请求模式定义"""
    method: str = Field(..., description="HTTP 方法", example="GET")
    url: str = Field(..., description="请求 URL", example="https://example.com")
    params: Optional[Dict[str, str]] = Field({}, description="查询参数")
    headers: Optional[Dict[str, str]] = Field({}, description="请求头")
    data: Optional[Union[str, Dict]] = Field(None, description="请求体数据")
    json_data: Optional[Dict] = Field(None, description="JSON 请求体数据")
    encoding: Optional[str] = Field(None, description="请求体的编码")

    @field_validator("method")
    def validate_method(cls, value: str) -> str:
        valid_methods = {
            "GET", "POST", "PUT", "DELETE", "PATCH",
            "HEAD", "OPTIONS", "CONNECT", "TRACE"
        }
        method = value.upper()
        if method not in valid_methods:
            raise ValueError(f"无效的 HTTP 方法: {value}")
        return method

def generate_encryption_key():
    """生成并存储加密密钥"""
    key = Fernet.generate_key()
    st.session_state.encryption_key = key.decode()
    st.success("新加密密钥已生成！")

def handle_api_key():
    """管理 API 密钥的会话状态"""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    st.session_state.api_key_input = st.text_input(
        "输入 API Key",
        value=st.session_state.api_key,
        on_change=lambda: setattr(
            st.session_state, "api_key", st.session_state.api_key_input
        )
    )

def send_http_request_ui(request: HTTPRequestSchema, encrypt: bool, encoding: str):
    """处理 HTTP 请求的 UI 交互"""
    progress_bar = st.progress(0)
    try:
        # 加密处理
        if encrypt:
            request = encrypt_request(request)
        
        # 发送请求
        response = asyncio.run(send_http_request(
            method=request.method,
            url=request.url,
            params=request.params,
            headers=request.headers,
            data=request.data,
            json=request.json_data,
            encoding=encoding,
        ))
        
        # 解密处理
        if encrypt:
            response = decrypt_response(response)
        
        # 展示结果
        display_response(response)
        
    except HTTPError as e:
        st.error(f"请求失败: {e.detail}")
    except Exception as e:
        st.error(f"请求异常: {str(e)}")
    finally:
        progress_bar.empty()

def encrypt_request(request: HTTPRequestSchema) -> HTTPRequestSchema:
    """请求数据加密"""
    encryptor = Fernet(st.session_state.encryption_key.encode())
    request.url = encrypt_data(request.url)
    request.params = {k: encrypt_data(v) for k, v in request.params.items()}
    request.headers = {k: encrypt_data(v) for k, v in request.headers.items()}
    if request.data:
        request.data = encrypt_data(request.data)
    if request.json_data:
        request.json_data = {k: encrypt_data(v) for k, v in request.json_data.items()}
    return request

def decrypt_response(response: HTTPResponseSchema) -> HTTPResponseSchema:
    """响应数据解密"""
    decryptor = Fernet(st.session_state.encryption_key.encode())
    response.text = decrypt_data(response.text)
    response.headers = {k: decrypt_data(v) for k, v in response.headers.items()}
    return response

def display_response(response: HTTPResponseSchema):
    """展示响应结果"""
    st.header("请求结果")
    st.write(f"状态码: {response.status_code}")
    st.write(f"响应时间: {response.elapsed:.2f} 秒")
    st.write("响应 Header:")
    st.json(response.headers)
    st.write("响应内容:")
    st.text(response.text)
    time.sleep(1)

# 初始化服务
mock_data_service = MockDataService()
task_scheduler = AsyncIOScheduler(jobstores={"default": MemoryJobStore()})

def run_ui():
    """主 UI 函数"""
    st.title("HTTP 请求模拟工具")

    # Mock 数据管理
    with st.expander("Mock 数据管理"):
        create_mock_data_section()
        retrieve_mock_data_section()
    
    # 任务调度
    with st.expander("任务调度"):
        schedule_task_section()
    
    # HTTP 请求表单
    method = st.selectbox("HTTP 方法", ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "TRACE"])
    url = st.text_input("URL")
    
    # 参数输入
    query_params = get_params("查询参数", "query_key", "query_value")
    form_params = get_params("表单参数", "form_key", "form_value")
    json_data = get_json_params()
    
    # Header 和 API Key
    headers = get_params("Header", "header_key", "header_value")
    handle_api_key()
    headers["x-api-key"] = st.session_state.api_key
    
    # 数据输入
    data = st.text_area("请求体数据")
    encoding = st.selectbox("编码方式", COMMON_ENCODINGS)
    
    # 加密选项
    encryption_enabled = st.checkbox("启用加密")
    if st.button("生成新密钥"):
        generate_encryption_key()
    display_encryption_key()
    
    # 发送请求
    if st.button("发送请求"):
        try:
            request = HTTPRequestSchema(
                method=method,
                url=url,
                params=query_params,
                headers=headers,
                data=data,
                json_data=json_data,
                encoding=encoding
            )
            send_http_request_ui(request, encryption_enabled, encoding)
        except ValidationError as e:
            st.error(f"参数验证失败: {e}")

    # 关闭按钮
    if st.button("关闭项目"):
        try:
            os.kill(os.getppid(), signal.SIGINT)
        except Exception as e:
            st.error(f"关闭失败: {e}")

def create_mock_data_section():
    """Mock 数据创建区域"""
    key = st.text_input("Key", key="mock_key")
    data = st.text_area("JSON 数据", key="mock_data")
    if st.button("创建"):
        try:
            mock_data_service.create_mock_data(key, json.loads(data))
            st.success("Mock 数据创建成功")
        except json.JSONDecodeError:
            st.error("JSON 格式错误")

def retrieve_mock_data_section():
    """Mock 数据获取区域"""
    key = st.text_input("Key", key="get_mock_key")
    if st.button("获取"):
        data = mock_data_service.get_mock_data(key)
        st.json(data) if data else st.warning("未找到数据")

def schedule_task_section():
    """任务调度区域"""
    url = st.text_input("URL", key="task_url")
    interval = st.number_input("间隔(秒)", 1, key="task_interval")
    if st.button("添加任务"):
        try:
            request = HTTPRequestSchema(method="GET", url=url)
            task_scheduler.add_job(
                send_http_request_ui,
                "interval",
                seconds=interval,
                args=[request, False, None]
            )
            task_scheduler.start()
            st.success("任务已添加")
        except ValidationError as e:
            st.error(f"参数错误: {e}")

def get_json_params() -> Optional[Dict]:
    """获取 JSON 参数"""
    json_str = st.text_area("JSON 参数", key="json_input")
    if json_str:
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            st.error("JSON 格式错误")
    return None

def display_encryption_key():
    """展示加密密钥"""
    if "encryption_key" in st.session_state:
        st.write(f"**密钥:** {st.session_state.encryption_key}")
        st.info("请妥善保管密钥！")

if __name__ == "__main__":
    run_ui()