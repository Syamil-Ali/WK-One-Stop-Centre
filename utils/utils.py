import re


# function validation url
def is_valid_url(url: str) -> bool:
    # Basic URL validation regex (you can customize further)
    regex = re.compile(
        r'^(https?|ftp)://'  # protocol
        r'[\w\-]+(\.[\w\-]+)+[/#?]?.*$',  # domain and path
        re.IGNORECASE,
    )
    return re.match(regex, url) is not None