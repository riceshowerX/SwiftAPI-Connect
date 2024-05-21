# progress_bar.py
import streamlit as st
import time

def show_progress_bar():
    """显示进度条"""
    progress_bar = st.progress(0)

    # 模拟请求处理时间
    for i in range(10):
        time.sleep(0.1)
        progress_bar.progress(i * 10)

    # 设置进度条为 100%
    progress_bar.progress(100)