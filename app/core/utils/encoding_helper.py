# encoding_helper.py
import logging
import chardet

DEFAULT_ENCODING = "utf-8"  # 设置默认编码

def decode_content(content: bytes, encoding: str = None, encoding_list: list = None) -> str:
    """
    解码字节内容，优先使用默认编码，如果解码失败，则尝试使用 chardet 检测编码。

    :param content: 要解码的字节内容
    :param encoding: 指定的编码格式，如果为空，则使用默认编码
    :return: 解码后的字符串
    """
    if encoding:
        try:
            logging.debug(f"Attempting to decode content with encoding: {encoding}")
            return content.decode(encoding)
        except UnicodeDecodeError as e:
            logging.warning(f"UnicodeDecodeError: {e}. Using default encoding ({DEFAULT_ENCODING}) and ignoring errors.")
            return content.decode(DEFAULT_ENCODING, errors="ignore")
    
    if encoding_list:
        for enc in encoding_list:
            try:
                logging.debug(f"Attempting to decode content with encoding: {enc}")
                return content.decode(enc)
            except UnicodeDecodeError:
                continue
    
    logging.warning(f"Trying to detect encoding with chardet.")
    detected_encoding = chardet.detect(content)['encoding']
    if detected_encoding:
        try:
            logging.debug(f"Detected encoding: {detected_encoding}")
            return content.decode(detected_encoding)
        except UnicodeDecodeError:
            logging.warning(f"Failed to decode content with detected encoding. Using default encoding ({DEFAULT_ENCODING}) and ignoring errors.")
            return content.decode(DEFAULT_ENCODING, errors="ignore")
    else:
        logging.warning(f"Failed to detect encoding. Using default encoding ({DEFAULT_ENCODING}) and ignoring errors.")
        return content.decode(DEFAULT_ENCODING, errors="ignore")