# encryption.py
import os
import base64
from typing import Tuple, Union
from Crypto.Cipher import AES, ChaCha20
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, ChaCha20Poly1305

class EncryptionError(Exception):
    """自定义加密错误异常"""
    pass

class EncryptionManager:
    def __init__(self, key: Union[bytes, None] = None, algorithm: str = 'AES-256-GCM'):
        if key is None:
            self.key = get_random_bytes(32)
        else:
            self.key = key
        self.algorithm = algorithm
        self.cipher_map = {
            'AES-256-CBC': (AES, AES.MODE_CBC),
            'AES-256-GCM': (AESGCM, None),
            'ChaCha20-Poly1305': (ChaCha20Poly1305, None),
        }

    def encrypt_data(self, data: str) -> Tuple[str, str]:
        """
        使用配置的加密算法对数据进行加密

        参数:
        data (str): 要加密的数据

        返回值:
        Tuple[str, str]: 初始化向量(IV)或随机数(nonce)和加密数据
        """
        try:
            cipher_class, mode = self.cipher_map[self.algorithm]
            if mode is None:
                # 对于AEAD加密模式,直接使用cipher_class加密
                cipher = cipher_class(self.key)
                nonce = cipher.nonce
                encrypted_data = cipher.encrypt(data.encode(), None)
                nonce = base64.b64encode(nonce).decode()
                encrypted_data = base64.b64encode(encrypted_data).decode()
            else:
                # 对于非AEAD加密模式,使用AES加密
                cipher = cipher_class.new(self.key, mode)
                encrypted_data = cipher.encrypt(pad(data.encode(), cipher_class.block_size))
                iv = base64.b64encode(cipher.iv).decode()
                encrypted_data = base64.b64encode(encrypted_data).decode()
                return iv, encrypted_data
        except KeyError:
            raise EncryptionError(f"不支持的加密算法: {self.algorithm}")
        except Exception as e:
            raise EncryptionError(f"加密数据时发生错误: {e}")

        return nonce, encrypted_data

    def decrypt_data(self, nonce_or_iv: str, encrypted_data: str) -> str:
        """
        使用配置的加密算法对加密数据进行解密

        参数:
        nonce_or_iv (str): 初始化向量(IV)或随机数(nonce)
        encrypted_data (str): 加密数据

        返回值:
        str: 解密后的数据
        """
        try:
            cipher_class, mode = self.cipher_map[self.algorithm]
            if mode is None:
                # 对于AEAD加密模式,直接使用cipher_class解密
                nonce = base64.b64decode(nonce_or_iv)
                encrypted_data = base64.b64decode(encrypted_data)
                cipher = cipher_class(self.key)
                decrypted_data = cipher.decrypt(nonce, encrypted_data, None)
            else:
                # 对于非AEAD加密模式,使用AES解密
                iv = base64.b64decode(nonce_or_iv)
                encrypted_data = base64.b64decode(encrypted_data)
                cipher = cipher_class.new(self.key, mode, iv)
                decrypted_data = unpad(cipher.decrypt(encrypted_data), cipher_class.block_size)
        except KeyError:
            raise EncryptionError(f"不支持的加密算法: {self.algorithm}")
        except Exception as e:
            raise EncryptionError(f"解密数据时发生错误: {e}")

        return decrypted_data.decode()