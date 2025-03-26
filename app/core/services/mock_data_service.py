from typing import Dict, Any
import json
import os

class MockDataService:
    def __init__(self, db_path: str = "mock_data.json"):
        self.db_path = db_path
        self._mock_data = {}
        self.load_data()

    def load_data(self) -> None:
        """从JSON文件加载数据，处理多种异常情况"""
        try:
            with open(self.db_path, 'r') as f:
                self._mock_data = json.load(f)
        except FileNotFoundError:
            self._mock_data = {}
        except (json.JSONDecodeError, IOError) as e:
            # 处理文件损坏或不可读的情况
            self._mock_data = {}
            self._log_error(f"数据加载失败: {str(e)}")

    def save_data(self) -> None:
        """将数据保存到JSON文件，添加错误处理"""
        try:
            with open(self.db_path, 'w') as f:
                json.dump(self._mock_data, f, indent=4)
        except IOError as e:
            self._log_error(f"数据保存失败: {str(e)}")

    def get_mock_data(self, key: str) -> Dict[str, Any]:
        """获取指定key的mock数据"""
        return self._mock_data.get(key)

    def create_mock_data(self, key: str, data: Dict) -> None:
        """创建新的mock数据，确保key唯一"""
        if key in self._mock_data:
            raise ValueError(f"Key '{key}' 已存在")
        self._mock_data[key] = data
        self.save_data()

    def update_mock_data(self, key: str, data: Dict) -> None:
        """更新现有mock数据"""
        if key not in self._mock_data:
            raise KeyError(f"Key '{key}' 不存在")
        self._mock_data[key] = data
        self.save_data()

    def delete_mock_data(self, key: str) -> None:
        """删除指定mock数据"""
        if key not in self._mock_data:
            raise KeyError(f"Key '{key}' 不存在")
        del self._mock_data[key]
        self.save_data()

    def _log_error(self, message: str) -> None:
        """统一错误日志记录"""
        print(f"ERROR: {message}")  # 可替换为实际日志系统