import logging
import chardet
from typing import Set

# 保留原有变量
DEFAULT_ENCODING = "utf-8"
COMMON_ENCODINGS = [
    "ascii", "utf-8", "utf-16", "utf-32", "latin-1",
    "gbk", "gb18030", "big5", "shift-jis", "euc-jp", "euc-kr"
]

class DecodingError(Exception):
    """自定义解码错误"""
    def __init__(self, message: str, tried_encodings: Set[str]):
        super().__init__(message)
        self.tried_encodings = tried_encodings

def decode_content(content: bytes, encoding: str = None) -> str:
    """
    智能解码字节内容，支持多编码策略
    
    Args:
        content: 待解码的字节内容
        encoding: 优先尝试的编码（可选）
        
    Returns:
        解码后的字符串
        
    Raises:
        DecodingError: 当所有解码尝试失败时抛出
    """
    tried_encodings = set()
    detected_encoding = None
    
    # 优先尝试用户指定编码或默认编码
    explicit_encodings = []
    if encoding:
        explicit_encodings.append(encoding)
    else:
        explicit_encodings.append(DEFAULT_ENCODING)
    
    # 创建编码尝试顺序：用户指定 -> 常用编码 -> 自动检测
    encodings_to_try = []
    for enc in explicit_encodings:
        if enc not in encodings_to_try:
            encodings_to_try.append(enc)
    
    for enc in COMMON_ENCODINGS:
        if enc not in encodings_to_try:
            encodings_to_try.append(enc)
    
    # 主解码流程
    try:
        # 第一阶段：显式指定的编码和常用编码
        for enc in encodings_to_try:
            if enc in tried_encodings:
                continue
            try:
                logging.debug(f"尝试解码使用编码: {enc}")
                return content.decode(enc)
            except UnicodeDecodeError:
                tried_encodings.add(enc)
        
        # 第二阶段：自动检测编码
        if not detected_encoding:
            detection = chardet.detect(content)
            detected_encoding = detection['encoding']
            confidence = detection['confidence']
            logging.debug(f"检测到编码: {detected_encoding} (置信度: {confidence:.2f})")
        
        if detected_encoding and detected_encoding not in tried_encodings:
            try:
                return content.decode(detected_encoding)
            except UnicodeDecodeError:
                tried_encodings.add(detected_encoding)
                
    except Exception as e:
        logging.error(f"解码过程中发生异常: {str(e)}")
        raise DecodingError(f"解码异常: {str(e)}", tried_encodings)
    
    # 所有尝试失败
    raise DecodingError(
        f"无法解码内容，已尝试编码: {sorted(tried_encodings)}", 
        tried_encodings
    )