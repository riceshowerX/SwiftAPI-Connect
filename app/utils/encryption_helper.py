# app/security/encryption_helper.py
from cryptography.fernet import Fernet
import logging

# 初始化日志记录器
logging.basicConfig(level=logging.INFO)

# 生成密钥
key = Fernet.generate_key()
f = Fernet(key)

# 加密请求数据
def encrypt_request(data: str) -> str:
    """
    使用 Fernet 对请求数据进行加密

    Args:
        data: 请求数据 (字符串)

    Returns:
        加密后的数据 (字符串)
    """
    encoded_data = data.encode()
    encrypted_data = f.encrypt(encoded_data)
    return encrypted_data.decode()

# 解密请求数据
def decrypt_request(data: str) -> str:
    """
    使用 Fernet 对加密后的请求数据进行解密

    Args:
        data: 加密后的数据 (字符串)

    Returns:
        解密后的数据 (字符串)
    """
    encrypted_data = data.encode()
    decrypted_data = f.decrypt(encrypted_data)
    return decrypted_data.decode()