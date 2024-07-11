# crypto.py
from cryptography.fernet import Fernet, InvalidToken
from typing import Union
import os
import logging
import secrets

# 尝试从环境变量读取 ENCRYPTION_KEY
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# 如果没有设置，则自动生成一个新的密钥并存储到环境变量
if ENCRYPTION_KEY is None:
    ENCRYPTION_KEY = secrets.token_urlsafe(32) 
    os.environ["ENCRYPTION_KEY"] = ENCRYPTION_KEY

# 将环境变量转换为字节类型
ENCRYPTION_KEY = ENCRYPTION_KEY.encode()  # 转换为字节类型

# 这里直接使用 ENCRYPTION_KEY
fernet = Fernet(ENCRYPTION_KEY) 

def encrypt_data(data: str) -> str:
    """加密数据"""
    try:
        return fernet.encrypt(data.encode()).decode()
    except Exception as e:
        logging.error(f"Encryption failed: {e}")
        raise  

def decrypt_data(data: str) -> Union[str, None]:
    """解密数据"""
    try:
        return fernet.decrypt(data.encode()).decode()
    except InvalidToken:
        logging.error("Decryption failed: Invalid token.")
        return None 
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        raise 