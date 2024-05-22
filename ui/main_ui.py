# main_ui.py
import os
import sys
import json
import logging
import time
import chardet

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将项目根目录添加到 PYTHONPATH
sys.path.append(project_root)

import streamlit as st

from app.core.utils.network_utils import send_http_request
from app.core.schemas.request_schema import HTTPRequestSchema
from app.core.schemas.response_schema import HTTPResponseSchema
from ui.components.param_input import ParamInput
from ui.components.progress_bar import show_progress_bar
from app.core.utils.crypto_utils import encrypt_data, decrypt_data

# 设置日志级别为 INFO
logging.basicConfig(level=logging.INFO)

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
    query_params = ParamInput("查询", "query_key", "query_value")
    form_params = ParamInput("表单", "form_key", "form_value")

    # JSON 参数
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
    headers = ParamInput("Header", "header_key", "header_value")

    # API Key 输入
    api_key = st.text_input("输入 API Key", key="api_key")
    headers["x-api-key"] = api_key

    # Data 输入区域
    st.header("Data")
    data = st.text_area("输入 Data", key="data_info")

    # 编码选择
    encoding = st.selectbox("选择编码", ["utf-8", "gbk", "latin-1"], key="encoding")

    # 加密选项区域
    st.header("加密选项")
    encryption_enabled = st.checkbox("开启加密", key="encryption_enabled")

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

            # 发送请求
            with st.spinner("发送请求中..."):
                response = send_http_request(
                    method=request_data.method,
                    url=request_data.url,
                    params=request_data.params,
                    headers=request_data.headers,
                    data=request_data.data,
                    json_data=request_data.json_data,
                    encoding=request_data.encoding,
                    encryption_enabled=encryption_enabled
                )

            # 处理响应
            if encryption_enabled:
                response.text = decrypt_data(response.content).decode(response.encoding)
            response_data = HTTPResponseSchema.from_attributes(response)

            # 展示结果
            st.header("请求结果")
            st.write(f"状态码: {response_data.status_code}")
            st.write(f"响应时间: {response_data.elapsed:.2f} 秒")
            st.write("响应 Header:")
            st.json(response_data.headers)
            st.write("响应内容:")
            st.text(response_data.text)

        except Exception as e:
            st.error(f"请求失败: {str(e)}")

if __name__ == "__main__":
    run_ui()