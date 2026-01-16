import re

def extract_features(url):
    url_length = len(url)
    has_https = 1 if "https" in url else 0
    num_digits = len(re.findall(r"\d", url))
    special_chars = len(re.findall(r"[!@#$%^&*(),.?\":{}|<>]", url))

    return [url_length, has_https, num_digits, special_chars]
