# crypto.py
from cryptography.fernet import Fernet, InvalidToken
from typing import Union
import os
import logging

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if ENCRYPTION_KEY is None:
    raise ValueError("ENCRYPTION_KEY environment variable is not set.")

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