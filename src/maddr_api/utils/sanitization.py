import re


def sanitization_string(input_string: str) -> str:
    """
    Sanitize input strings by removing special characters and normalizing whitespace.
    """
    sanitized = re.sub(r"[^a-zA-Z0-9 ]", "", input_string)
    sanitized = sanitized.strip().lower()
    sanitized = re.sub(r"\s+", " ", sanitized)
    return sanitized
