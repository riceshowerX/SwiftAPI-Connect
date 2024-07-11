# encoding_helper.py
import logging
import chardet

DEFAULT_ENCODING = "utf-8"
COMMON_ENCODINGS = ["ascii", "utf-8", "utf-16", "utf-32", "latin-1", "gbk", "gb18030", "big5", "shift-jis", "euc-jp", "euc-kr"]

class DecodingError(Exception):
    """自定义解码错误"""
    def __init__(self, message, tried_encodings):
        super().__init__(message)
        self.tried_encodings = tried_encodings

def decode_content(content: bytes, encoding: str = None) -> str:
    """
    解码字节内容，优先使用指定的编码，如果解码失败，则尝试使用 chardet 检测编码。

    :param content: 要解码的字节内容
    :param encoding: 指定的编码格式，如果为空，则使用默认编码
    :return: 解码后的字符串
    :raises DecodingError: 解码失败
    """
    tried_encodings = []
    if encoding is not None:
        tried_encodings.append(encoding)

    # 尝试使用指定的编码或默认编码解码
    for enc in tried_encodings + COMMON_ENCODINGS:
        try:
            logging.debug(f"Attempting to decode content with encoding: {enc}")
            return content.decode(enc)
        except UnicodeDecodeError as e:
            logging.warning(f"UnicodeDecodeError: {e}. Trying next encoding.")

    # 如果所有编码都尝试失败，则使用 chardet 检测编码
    detected_encoding = chardet.detect(content)['encoding']
    if detected_encoding is not None:
        tried_encodings.append(detected_encoding)
        try:
            logging.debug(f"Detected encoding: {detected_encoding}")
            return content.decode(detected_encoding)
        except UnicodeDecodeError as e:
            logging.warning(f"Failed to decode content with detected encoding: {e}")

    # 所有尝试都失败，抛出自定义异常
    raise DecodingError(f"Failed to decode content. Tried encodings: {tried_encodings}", tried_encodings)