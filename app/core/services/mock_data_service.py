# mock_data_service.py
# 此文件定义与 Mock 数据管理相关的服务
from typing import List, Dict

class MockDataService:
    def __init__(self):
        # 初始化数据存储，例如使用字典或数据库连接
        self.mock_data = {}

    def get_mock_data(self, key: str) -> Dict:
        # 获取指定 key 的 Mock 数据
        return self.mock_data.get(key)

    def create_mock_data(self, key: str, data: Dict):
        # 创建新的 Mock 数据
        self.mock_data[key] = data

    def update_mock_data(self, key: str, data: Dict):
        # 更新 Mock 数据
        if key in self.mock_data:
            self.mock_data[key] = data

    def delete_mock_data(self, key: str):
        # 删除 Mock 数据
        if key in self.mock_data:
            del self.mock_data[key]