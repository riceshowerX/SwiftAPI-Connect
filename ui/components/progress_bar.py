# progress_bar.py
import streamlit as st
import asyncio
import time

async def show_progress_bar(get_progress=lambda: 100):
    """显示进度条，使用异步函数避免阻塞主线程。

    Args:
        get_progress: 一个回调函数，返回当前操作的进度 (0-100).
    """
    progress_bar = st.progress(0)

    while True:
        try:
            progress = get_progress()
        except Exception as e:
            st.error(f"获取进度失败: {e}")
            break

        progress_bar.progress(progress)

        if progress >= 100:
            break

        await asyncio.sleep(0.1)  # 调整更新频率