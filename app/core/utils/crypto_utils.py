# crypto_utils.py
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量中获取加密密钥
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# 如果没有设置加密密钥，则抛出异常
if ENCRYPTION_KEY is None:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")

# 创建 Fernet 对象
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: bytes) -> bytes:
    """加密数据"""
    return fernet.encrypt(data)


def decrypt_data(data: bytes) -> bytes:
    """解密数据"""
    return fernet.decrypt(data)