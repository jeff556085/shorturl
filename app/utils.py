import re

def is_valid_url(url: str) -> bool:
    pattern = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,6}' 
        r'(?:[/?#][^\s]*)?$', re.IGNORECASE)
    return re.match(pattern, url) is not None