def decode_content(content, encoding):
    if encoding:
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            return content.decode("utf-8", errors="ignore")
    return content