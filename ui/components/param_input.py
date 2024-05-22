# param_input.py
import streamlit as st

def ParamInput(param_type, key_prefix, value_prefix):
    params = {}
    with st.expander(f"{param_type} 参数"):
        param_count = st.number_input(
            f"{param_type} 参数数量", min_value=0, step=1, key=f"{param_type}_params_count"
        )
        for i in range(param_count):
            col1, col2, col3 = st.columns(3)
            with col1:
                key = st.text_input(
                    f"{param_type} 参数 {i+1} 的 Key", key=f"{key_prefix}_{i}"
                )
            with col2:
                param_type = st.selectbox("选择参数类型", ["string", "integer", "float", "boolean"], key=f"param_type_{i}")
            with col3:
                if param_type == "string":
                    value = st.text_input(f"{param_type} 参数 {i+1} 的 Value", key=f"{value_prefix}_{i}")
                elif param_type == "integer":
                    value = st.number_input(f"{param_type} 参数 {i+1} 的 Value", step=1, key=f"{value_prefix}_{i}")
                elif param_type == "float":
                    value = st.number_input(f"{param_type} 参数 {i+1} 的 Value", key=f"{value_prefix}_{i}")
                elif param_type == "boolean":
                    value = st.checkbox(f"{param_type} 参数 {i+1} 的 Value", key=f"{value_prefix}_{i}")
                else:
                    value = st.text_input(f"{param_type} 参数 {i+1} 的 Value", key=f"{value_prefix}_{i}")
            params[key] = value
    return params