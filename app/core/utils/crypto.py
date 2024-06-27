# crypto.py
# crypto.py
from cryptography.fernet import Fernet, InvalidToken
from typing import Union
import os
import logging
import zlib

# 尝试从环境变量读取 ENCRYPTION_KEY
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

# 如果没有设置，则自动生成一个新的密钥并存储到环境变量
if ENCRYPTION_KEY is None:
    ENCRYPTION_KEY = Fernet.generate_key().decode()  # 使用Fernet生成的密钥
    os.environ["ENCRYPTION_KEY"] = ENCRYPTION_KEY

fernet = Fernet(ENCRYPTION_KEY.encode())  # 将密钥转换为字节类型

def compress_data(data: str) -> bytes:
    """压缩数据"""
    return zlib.compress(data.encode())

def decompress_data(data: bytes) -> str:
    """解压数据"""
    return zlib.decompress(data).decode()

def encrypt_data(data: str) -> str:
    """加密数据"""
    try:
        compressed_data = compress_data(data)
        encrypted_data = fernet.encrypt(compressed_data)
        return encrypted_data.decode()
    except Exception as e:
        logging.error(f"Encryption failed: {e}")
        raise  

def decrypt_data(data: str) -> Union[str, None]:
    """解密数据"""
    try:
        decrypted_data = fernet.decrypt(data.encode())
        return decompress_data(decrypted_data)
    except InvalidToken:
        logging.error("Decryption failed: Invalid token.")
        return None 
    except Exception as e:
        logging.error(f"Decryption failed: {e}")
        raise  
