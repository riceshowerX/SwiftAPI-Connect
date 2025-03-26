from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from typing import Optional
import logging

# 单例模式存储调度器实例
_scheduler: Optional[AsyncIOScheduler] = None

def get_scheduler() -> AsyncIOScheduler:
    """获取或创建全局调度器实例"""
    global _scheduler
    if _scheduler is None:
        try:
            # 配置作业存储和执行器
            jobstores = {
                'default': MemoryJobStore()
            }
            executors = {
                'default': ThreadPoolExecutor(20),
                'processpool': ProcessPoolExecutor(5)
            }
            # 初始化调度器
            _scheduler = AsyncIOScheduler(
                jobstores=jobstores,
                executors=executors,
                timezone='UTC'  # 使用UTC时区避免时区问题
            )
            logging.info("任务调度器初始化成功")
        except Exception as e:
            logging.error(f"任务调度器初始化失败: {e}")
            raise
    return _scheduler

def start_scheduler() -> None:
    """安全启动调度器"""
    scheduler = get_scheduler()
    if not scheduler.running:
        try:
            scheduler.start()
            logging.info("任务调度器已启动")
        except Exception as e:
            logging.error(f"无法启动调度器: {e}")
            raise

def shutdown_scheduler() -> None:
    """优雅关闭调度器"""
    global _scheduler
    if _scheduler and _scheduler.running:
        try:
            _scheduler.shutdown()
            logging.info("任务调度器已关闭")
        except Exception as e:
            logging.error(f"调度器关闭失败: {e}")
        finally:
            _scheduler = None