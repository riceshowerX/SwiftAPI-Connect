"""
示例插件模块
"""
from fastapi import Request
from fastapi.responses import HTMLResponse
from app.plugins.base_plugin import BasePlugin

class ExamplePlugin(BasePlugin):
    """
    示例插件
    """
    def setup_routes(self):
        self.router.add_api_route("/example", self.example_endpoint, methods=["GET"])

    async def example_endpoint(self, request: Request):
        return HTMLResponse("<h1>Hello from Example Plugin!</h1>")