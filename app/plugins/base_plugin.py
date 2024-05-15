"""
插件基类
"""
from fastapi import APIRouter

class BasePlugin:
    """
    所有插件的基类
    """
    def __init__(self):
        self.router = APIRouter()
        self.setup_routes()

    def setup_routes(self):
        """
        设置插件的路由
        """
        raise NotImplementedError