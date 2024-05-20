# encoding_helper.py
import logging

def decode_content(content, encoding):
    """
    根据指定的编码解码内容。如果解码失败，尝试使用 UTF-8 解码并忽略错误。

    :param content: 要解码的字节内容
    :param encoding: 指定的编码格式
    :return: 解码后的字符串，如果解码失败，则返回原始的字节内容
    """
    if encoding:
        try:
            logging.debug(f"Attempting to decode content with encoding: {encoding}")
            return content.decode(encoding)
        except UnicodeDecodeError as e:
            logging.error(f"UnicodeDecodeError: {e}. Trying to decode with UTF-8 and ignore errors.")
            try:
                return content.decode("utf-8", errors="ignore")
            except UnicodeDecodeError as e:
                logging.error(f"Failed to decode content with UTF-8: {e}. Returning original bytes.")
    return content
