import streamlit as st

def get_params(param_type: str, key_prefix: str, value_prefix: str) -> dict:
    """
    动态生成参数输入组件并返回参数字典
    :param param_type: 参数类型标识（如"查询"、"表单"）
    :param key_prefix: Key输入框的前缀
    :param value_prefix: Value输入框的前缀
    :return: 包含有效参数的字典
    """
    params = {}
    warnings = []
    
    with st.expander(f"{param_type} 参数配置"):
        # 参数数量控制
        param_count = st.number_input(
            f"{param_type} 参数数量",
            min_value=0,
            step=1,
            key=f"{param_type.lower()}_param_count"
        )
        
        for i in range(param_count):
            # 创建参数输入行
            key_col, value_col = st.columns([3, 7])
            with key_col:
                current_key = st.text_input(
                    f"参数 {i+1} 的 Key",
                    key=f"{key_prefix}_{i}",
                    placeholder=f"{param_type}Key"
                )
            with value_col:
                current_value = st.text_input(
                    f"参数 {i+1} 的 Value",
                    key=f"{value_prefix}_{i}",
                    placeholder=f"{param_type}Value"
                )
            
            # 数据校验
            if current_key.strip():
                params[current_key] = current_value
            else:
                warnings.append(f"第 {i+1} 个{param_type}参数的Key不能为空")
        
        # 批量显示警告信息
        if warnings:
            st.warning("\n".join(warnings))
    
    return params