# task_scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import logging
import atexit
import os

# 日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 从环境变量或配置文件读取调度器配置
jobstore = MemoryJobStore()
executors = {
    'default': ThreadPoolExecutor(20)  # 可以根据需要调整线程池大小
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

# 初始化调度器
scheduler = AsyncIOScheduler(jobstores={'default': jobstore}, executors=executors, job_defaults=job_defaults, timezone=os.getenv('TZ', 'UTC'))

def graceful_shutdown():
    """优雅关闭调度器"""
    logging.info("Shutting down scheduler...")
    scheduler.shutdown(wait=True)
    logging.info("Scheduler shut down successfully.")

# 注册优雅关闭函数
atexit.register(graceful_shutdown)

# 启动调度器
scheduler.start()
logging.info("Scheduler started successfully.")

# 示例任务
def example_task():
    logging.info("Executing example task...")

# 添加示例任务
scheduler.add_job(example_task, 'interval', seconds=30, id='example_task', replace_existing=True)
logging.info("Example task added to scheduler.")

# 如果需要在其他模块中使用scheduler，可以将其暴露出来
__all__ = ['scheduler']
