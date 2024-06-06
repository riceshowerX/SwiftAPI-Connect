# progress_bar.py
import streamlit as st
import time

def show_progress_bar(get_progress=lambda: 100):
    """显示进度条
    
    Args:
        get_progress: 一个回调函数，返回当前操作的进度 (0-100).
    """
    progress_bar = st.progress(0)

    while True:
        progress = get_progress()
        progress_bar.progress(progress)

        if progress >= 100:
            break
        
        time.sleep(0.1)  # 调整更新频率