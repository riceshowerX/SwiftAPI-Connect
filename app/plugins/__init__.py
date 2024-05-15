"""
插件模块的初始化文件
"""
from importlib import import_module
from pathlib import Path
from typing import List
from app.plugins.base_plugin import BasePlugin

def load_plugins() -> List[BasePlugin]:
    """
    加载所有插件模块
    """
    plugins = []
    plugins_dir = Path(__file__).parent
    for file in plugins_dir.iterdir():
        if file.is_file() and file.suffix == ".py" and file.stem != "base_plugin" and not file.stem.startswith("_"):
            module = import_module(f"app.plugins.{file.stem}")
            plugin_class_name = file.stem.capitalize() + "Plugin"
            plugin_class = getattr(module, plugin_class_name)
            plugins.append(plugin_class())
    return plugins
