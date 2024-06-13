# task_scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore

# 初始化调度器，使用内存存储任务
scheduler = AsyncIOScheduler(jobstores={"default": MemoryJobStore()})