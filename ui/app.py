# app.py
import streamlit as st
import requests
import json

def run_ui():  # 定义一个可调用的函数
    st.title("HTTP 请求模拟工具")

    # 选择 HTTP 方法
    method = st.selectbox("选择 HTTP 方法", ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS", "TRACE"])

    # 输入 URL
    url = st.text_input("输入 URL")

    # 参数输入区域
    st.header("参数")
    params = {}
    with st.expander("查询参数"):
        for i in range(st.number_input("参数数量", min_value=0, step=1)):
            col1, col2 = st.columns(2)
            with col1:
                key = st.text_input(f"参数 {i+1} 的 Key")
            with col2:
                value = st.text_input(f"参数 {i+1} 的 Value")
            params[key] = value

    with st.expander("表单参数"):
        for i in range(st.number_input("参数数量", min_value=0, step=1, key="form_params")):
            col1, col2 = st.columns(2)
            with col1:
                key = st.text_input(f"参数 {i+1} 的 Key", key=f"form_key_{i}")
            with col2:
                value = st.text_input(f"参数 {i+1} 的 Value", key=f"form_value_{i}")
            params[key] = value

    with st.expander("JSON 参数"):
        json_str = st.text_area("输入 JSON 字符串", key="json_data")
        if json_str:
            try:
                json_data = json.loads(json_str)
            except json.JSONDecodeError:
                st.error("JSON 格式错误！")
                json_data = None

    # Header 输入区域
    st.header("Header")
    headers = {}
    with st.expander("Header 信息"):
        for i in range(st.number_input("Header 数量", min_value=0, step=1, key="header_count")):
            col1, col2 = st.columns(2)
            with col1:
                key = st.text_input(f"Header {i+1} 的 Key", key=f"header_key_{i}")
            with col2:
                value = st.text_input(f"Header {i+1} 的 Value", key=f"header_value_{i}")
            headers[key] = value

    # Data 输入区域
    st.header("Data")
    data = None
    with st.expander("Data 信息"):
        data_str = st.text_area("输入 Data", key="data_info")
        if data_str:
            data = data_str

    # 编码选择
    encoding = st.selectbox("选择编码", ["UTF-8", "GBK", "GB2312", "GB18030"])

    # 发送请求按钮
    if st.button("发送请求"):
        try:
            if method == "GET":
                response = requests.get(url, params=params, headers=headers)
            elif method == "POST":
                if json_data:
                    response = requests.post(url, json=json_data, headers=headers)  # 使用 json_data
                else:
                    response = requests.post(url, data=data, headers=headers)
            elif method == "PUT":
                if json_data:
                    response = requests.put(url, json=json_data, headers=headers)   # 使用 json_data
                else:
                    response = requests.put(url, data=data, headers=headers)
            elif method == "DELETE":
                response = requests.delete(url, headers=headers)
            elif method == "HEAD":
                response = requests.head(url, headers=headers)
            elif method == "OPTIONS":
                response = requests.options(url, headers=headers)
            else: # method == "TRACE":
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

if __name__ == "__main__":
    run_ui()