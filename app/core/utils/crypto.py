# crypto.py
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量中获取加密密钥
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# 如果没有设置加密密钥，则生成一个新的密钥
if ENCRYPTION_KEY is None:
    ENCRYPTION_KEY = Fernet.generate_key()
    with open(".env", "a") as f:
        f.write(f"\nENCRYPTION_KEY={ENCRYPTION_KEY.decode()}\n")

# 创建 Fernet 对象
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """加密数据"""
    return fernet.encrypt(data.encode()).decode()


def decrypt_data(data: str) -> str:
    """解密数据"""
    return fernet.decrypt(data.encode()).decode()