# progress_bar.py
import streamlit as st
import asyncio

async def show_progress_bar(get_progress=lambda: 100):
    """显示进度条，使用异步函数避免阻塞主线程。

    Args:
        get_progress (Callable[[], int]): 一个回调函数，返回当前操作的进度 (0-100).
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
            st.success("操作完成！")
            break

        await asyncio.sleep(0.1)  # 调整更新频率

# 示例使用
async def example_progress():
    for i in range(101):
        yield i
        await asyncio.sleep(0.05)

def get_example_progress():
    if not hasattr(get_example_progress, "progress"):
        get_example_progress.progress = example_progress()
    return next(get_example_progress.progress, 100)

# 在 Streamlit 中运行进度条
if __name__ == "__main__":
    st.title("进度条示例")
    asyncio.run(show_progress_bar(get_example_progress))