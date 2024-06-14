# mock_data_service.py
from typing import Dict
import json
import os
import logging
from tempfile import NamedTemporaryFile
import shutil

class MockDataService:
    def __init__(self, db_path="mock_data.json"):
        self.db_path = db_path
        self.load_data()
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def load_data(self):
        """从 JSON 文件加载数据"""
        try:
            with open(self.db_path, 'r') as f:
                self.mock_data = json.load(f)
            logging.info("数据加载成功")
        except FileNotFoundError:
            self.mock_data = {}
            logging.warning("文件未找到，初始化为空数据")
        except json.JSONDecodeError:
            self.mock_data = {}
            logging.error("文件解码错误，初始化为空数据")

    def save_data(self):
        """保存数据到 JSON 文件"""
        try:
            with NamedTemporaryFile('w', delete=False) as temp_file:
                json.dump(self.mock_data, temp_file, indent=4)
                temp_file.flush()
                os.fsync(temp_file.fileno())
            shutil.move(temp_file.name, self.db_path)
            logging.info("数据保存成功")
        except Exception as e:
            logging.error(f"保存数据时出错: {e}")

    def get_mock_data(self, key: str) -> Dict:
        """获取指定 key 的 Mock 数据"""
        return self.mock_data.get(key)

    def create_mock_data(self, key: str, data: Dict):
        """创建新的 Mock 数据"""
        if key in self.mock_data:
            raise ValueError(f"Mock 数据键 '{key}' 已存在。")
        self.mock_data[key] = data
        self.save_data()
        logging.info(f"创建数据: {key}")

    def update_mock_data(self, key: str, data: Dict):
        """更新 Mock 数据"""
        if key not in self.mock_data:
            raise KeyError(f"Mock 数据键 '{key}' 未找到。")
        self.mock_data[key] = data
        self.save_data()
        logging.info(f"更新数据: {key}")

    def delete_mock_data(self, key: str):
        """删除 Mock 数据"""
        if key not in self.mock_data:
            raise KeyError(f"Mock 数据键 '{key}' 未找到。")
        del self.mock_data[key]
        self.save_data()
        logging.info(f"删除数据: {key}")
