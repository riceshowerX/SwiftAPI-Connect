# crypto.py
from cryptography.fernet import Fernet
import base64
import logging
import os

# 设置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s")
logger = logging.getLogger(__name__)

# 从环境变量获取密钥
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY")
if not ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")

def generate_key():
    """生成密钥"""
    key = Fernet.generate_key()
    return key

def encrypt_data(data: bytes) -> str:
    """加密数据"""
    try:
        f = Fernet(ENCRYPTION_KEY)
        encrypted_data = f.encrypt(data)
        return base64.b64encode(encrypted_data).decode()
    except Exception as e:
        logger.error(f"Error encrypting data: {e}")
        raise

def decrypt_data(encrypted_data: str) -> bytes:
    """解密数据"""
    try:
        f = Fernet(ENCRYPTION_KEY)
        encrypted_data = base64.b64decode(encrypted_data.encode())
        decrypted_data = f.decrypt(encrypted_data)
        return decrypted_data
    except Exception as e:
        logger.error(f"Error decrypting data: {e}")
        raise