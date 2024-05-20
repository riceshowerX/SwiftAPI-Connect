# app.py
import streamlit as st
import requests
import json
import logging

logging.basicConfig(level=logging.INFO)

def get_params(param_type, key_prefix, value_prefix):
    params = {}
    with st.expander(f"{param_type} 参数"):
        param_count = st.number_input(f"{param_type} 参数数量", min_value=0, step=1, key=f"{param_type}_params_count")
        for i in range(param_count):
            col1, col2 = st.columns(2)
            with col1:
                key = st.text_input(f"{param_type} 参数 {i+1} 的 Key", key=f"{key_prefix}_{i}")
            with col2:
                value = st.text_input(f"{param_type} 参数 {i+1} 的 Value", key=f"{value_prefix}_{i}")
            params[key] = value
    return params

def run_ui():
    st.title("HTTP 请求模拟工具")

    # 选择 HTTP 方法
    method = st.selectbox("选择 HTTP 方法", ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "TRACE"])

    # 输入 URL
    url = st.text_input("输入 URL")

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

    # Data 输入区域
    st.header("Data")
    data = st.text_area("输入 Data", key="data_info")

    # 编码选择
    encoding = st.selectbox("选择编码", ["UTF-8", "GBK", "GB2312", "GB18030"])

    # 发送请求按钮
    if st.button("发送请求"):
        try:
            response = None
            if method == "GET":
                response = requests.get(url, params=query_params, headers=headers)
            elif method == "POST":
                if json_data:
                    response = requests.post(url, json=json_data, headers=headers)
                else:
                    response = requests.post(url, data=data, headers=headers)
            elif method == "PUT":
                if json_data:
                    response = requests.put(url, json=json_data, headers=headers)
                else:
                    response = requests.put(url, data=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            elif method == "HEAD":
                response = requests.head(url, headers=headers)
            elif method == "OPTIONS":
                response = requests.options(url, headers=headers)
            elif method == "TRACE":
                response = requests.request("TRACE", url, headers=headers)

            # 展示结果
            st.header("请求结果")
            st.write(f"状态码: {response.status_code}")
            st.write(f"响应时间: {response.elapsed.total_seconds()} 秒")
            st.write("响应 Header:")
            st.json(dict(response.headers))
            st.write("响应内容:")
            st.text(response.text)

        except Exception as e:
            st.error(f"请求失败: {str(e)}")
            logging.error(f"Request failed: {e}")

if __name__ == "__main__":
    run_ui()
