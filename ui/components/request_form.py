# request_form.py
import streamlit as st

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