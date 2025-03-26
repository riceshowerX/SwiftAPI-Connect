import streamlit as st
import asyncio
from typing import Callable

async def show_progress_bar(get_progress: Callable[[], int] = lambda: 100) -> None:
    """显示异步进度条，自动处理边界值和异常
    
    Args:
        get_progress: 返回当前进度百分比的回调函数（0-100）
    """
    progress_bar = st.progress(0)
    error_occurred = False

    try:
        while True:
            try:
                # 获取并校正进度值
                raw_progress = get_progress()
                progress = max(0, min(raw_progress, 100))
                
                # 更新进度条
                progress_bar.progress(progress)
                
                if progress >= 100:
                    break
                    
                await asyncio.sleep(0.1)
                    
            except asyncio.CancelledError:
                # 处理任务取消
                st.warning("进度更新已取消")
                break
            except Exception as e:
                # 记录错误但继续运行
                st.error(f"进度更新失败: {str(e)}")
                error_occurred = True
                break

    finally:
        # 确保最终状态为100%
        if not error_occurred:
            progress_bar.progress(100)
        progress_bar.empty()  # 清理组件