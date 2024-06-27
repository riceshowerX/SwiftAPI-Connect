# request_form.py
import streamlit as st
from typing import Dict

def get_params(param_type: str, key_prefix: str, value_prefix: str) -> Dict[str, str]:
    """生成一个动态表单，用于获取 HTTP 请求的参数。

    Args:
        param_type (str): 参数类型（例如，查询参数、请求头）。
        key_prefix (str): 用于 key 输入框的前缀。
        value_prefix (str): 用于 value 输入框的前缀。

    Returns:
        Dict[str, str]: 包含所有参数的字典。
    """
    params = {}
    with st.expander(f"{param_type} 参数"):
        param_count = st.number_input(
            f"{param_type} 参数数量", min_value=0, step=1, key=f"{param_type}_params_count", value=0
        )
        for i in range(param_count):
            col1, col2 = st.columns(2)
            with col1:
                key = st.text_input(
                    f"{param_type} 参数 {i+1} 的 Key", key=f"{key_prefix}_{i}",
                    placeholder="请输入参数名"
                )
            with col2:
                value = st.text_input(
                    f"{param_type} 参数 {i+1} 的 Value", key=f"{value_prefix}_{i}",
                    placeholder="请输入参数值"
                )
            # 简单的数据校验: key 不能为空
            if key:
                params[key] = value 
            else:
                st.warning(f"{param_type} 参数 {i+1} 的 Key 不能为空，请输入参数名")
    return params

# 示例使用
if __name__ == "__main__":
    st.title("HTTP 请求参数输入表单")
    query_params = get_params("查询", "query_key", "query_value")
    header_params = get_params("请求头", "header_key", "header_value")

    if st.button("提交"):
        st.write("查询参数:", query_params)
        st.write("请求头参数:", header_params)