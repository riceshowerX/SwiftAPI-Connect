# progress_bar.py
import streamlit as st
import time

def show_progress_bar():
    """显示进度条"""
    progress_bar = st.progress(0)
    for i in range(101):
        time.sleep(0.01)  # 模拟耗时操作
        progress_bar.progress(i)