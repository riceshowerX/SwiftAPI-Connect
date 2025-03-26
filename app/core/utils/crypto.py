from cryptography.fernet import Fernet, InvalidToken
from typing import Optional
import os
import logging
import secrets

# 初始化日志记录器
logger = logging.getLogger(__name__)

# 密钥配置优化
def _initialize_encryption_key() -> bytes:
    """密钥初始化逻辑"""
    key = os.getenv("ENCRYPTION_KEY")
    
    if not key:
        logger.warning("未检测到加密密钥，正在生成新密钥")
        key = Fernet.generate_key().decode()  # 使用Fernet标准密钥生成方式
        os.environ["ENCRYPTION_KEY"] = key
        logger.info("新密钥已生成并存储到环境变量")
    else:
        # 验证密钥有效性
        try:
            Fernet(key.encode())
        except Exception as e:
            logger.error(f"无效的加密密钥: {e}")
            raise ValueError("无效的ENCRYPTION_KEY环境变量") from e
    
    return key.encode()

# 延迟初始化密钥和Fernet实例
_ENCRYPTION_KEY = _initialize_encryption_key()
_fernet = Fernet(_ENCRYPTION_KEY)

def encrypt_data(data: str) -> str:
    """加密数据（使用URL安全的Base64编码）
    
    Args:
        data: 需要加密的明文数据
    
    Returns:
        加密后的字符串
    
    Raises:
        ValueError: 密钥无效时
        cryptography.exceptions.EncryptionError: 加密失败时
    """
    try:
        return _fernet.encrypt(data.encode()).decode()
    except Exception as e:
        logger.error(f"加密失败: {str(e)}", exc_info=True)
        raise

def decrypt_data(encrypted_data: str) -> Optional[str]:
    """解密数据
    
    Args:
        encrypted_data: 加密后的字符串
    
    Returns:
        解密后的明文，验证失败时返回None
    
    Raises:
        cryptography.fernet.InvalidToken: 密文无效时
        ValueError: 密钥无效时
    """
    try:
        return _fernet.decrypt(encrypted_data.encode()).decode()
    except InvalidToken:
        logger.warning("解密失败：无效的加密数据")
        return None
    except Exception as e:
        logger.error(f"解密失败: {str(e)}", exc_info=True)
        raise