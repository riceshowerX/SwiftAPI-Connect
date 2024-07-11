# mock_data_service.py
from typing import List, Dict
import json
import os

class MockDataService:
    def __init__(self, db_path="mock_data.json"):
        self.db_path = db_path
        self.load_data()

    def load_data(self):
        """从 JSON 文件加载数据"""
        try:
            with open(self.db_path, 'r') as f:
                self.mock_data = json.load(f)
        except FileNotFoundError:
            self.mock_data = {}

    def save_data(self):
        """保存数据到 JSON 文件"""
        with open(self.db_path, 'w') as f:
            json.dump(self.mock_data, f, indent=4)

    def get_mock_data(self, key: str) -> Dict:
        # 获取指定 key 的 Mock 数据
        return self.mock_data.get(key)

    def create_mock_data(self, key: str, data: Dict):
        # 创建新的 Mock 数据
        if key in self.mock_data:
            raise ValueError(f"Mock data with key '{key}' already exists.")
        self.mock_data[key] = data
        self.save_data()

    def update_mock_data(self, key: str, data: Dict):
        # 更新 Mock 数据
        if key not in self.mock_data:
            raise KeyError(f"Mock data with key '{key}' not found.")
        self.mock_data[key] = data
        self.save_data()