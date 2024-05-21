# encoding_helper.py
import logging

DEFAULT_ENCODING = "utf-8"  # 设置默认编码

def decode_content(content, encoding=None):
    """
    根据指定的编码解码内容。如果解码失败，尝试使用默认编码解码并忽略错误。

    :param content: 要解码的字节内容
    :param encoding: 指定的编码格式，如果为空，则使用默认编码
    :return: 解码后的字符串，如果解码失败，则返回原始的字节内容
    """

    encoding = encoding or DEFAULT_ENCODING  # 使用默认编码
    try:
        logging.debug(f"Attempting to decode content with encoding: {encoding}")
        return content.decode(encoding)
    except UnicodeDecodeError as e:
        logging.warning(f"UnicodeDecodeError: {e}. Trying to decode with {DEFAULT_ENCODING} and ignore errors.")
        try:
            return content.decode(DEFAULT_ENCODING, errors="ignore")
        except UnicodeDecodeError as e:
            logging.error(f"Failed to decode content with {DEFAULT_ENCODING}: {e}. Returning original bytes.")
    return content