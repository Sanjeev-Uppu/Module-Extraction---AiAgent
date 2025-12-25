import re

def validate_url(url: str) -> bool:
    """
    Validates whether the input string is a proper HTTP/HTTPS URL
    """
    pattern = re.compile(r"^https?://")
    return bool(pattern.match(url))
