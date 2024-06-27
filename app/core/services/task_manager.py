# notification_service.py
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import os

from app.core.config import settings

class TaskManager:
    """
    任务管理类，负责调度任务
    """

    def __init__(self):
        # 初始化调度器
        self.scheduler = AsyncIOScheduler(
            jobstores={"default": MemoryJobStore()},
            executors={
                'default': ThreadPoolExecutor(20)  # 可以根据需要调整线程池大小
            },
            job_defaults={
                'coalesce': False,
                'max_instances': 3
            },
            timezone=os.getenv('TZ', 'UTC')
        )
        self.scheduler.start()
        logging.info("Scheduler started successfully.")

    def add_task(self, func, trigger, **kwargs):
        """添加任务"""
        job_id = kwargs.get('id', str(uuid.uuid4()))
        self.scheduler.add_job(func, trigger, id=job_id, replace_existing=True, **kwargs)
        logging.info(f"Added task: {job_id}")

    def remove_task(self, job_id):
        """删除任务"""
        self.scheduler.remove_job(job_id)
        logging.info(f"Removed task: {job_id}")

    def get_jobs(self):
        """获取所有任务"""
        return self.scheduler.get_jobs()

# 实例化任务管理器
task_manager = TaskManager()