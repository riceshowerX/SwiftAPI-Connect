# task_scheduler.py
# 此文件定义与任务调度相关的服务
import asyncio

class TaskScheduler:
    def __init__(self):
        # 初始化任务队列
        self.tasks = []

    def add_task(self, task):
        # 添加任务到队列
        self.tasks.append(task)

    async def run_tasks(self):
        # 运行所有任务
        await asyncio.gather(*self.tasks)