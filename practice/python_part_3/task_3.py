"""
Write a function which detects if entered string is http/https domain name with optional slash at the and
Restriction: use re module
Note that address may have several domain levels
    >>>is_http_domain('http://wikipedia.org')
    True
    >>>is_http_domain('https://ru.wikipedia.org/')
    True
    >>>is_http_domain('griddynamics.com')
    False
"""

import re


def is_http_domain(domain: str) -> bool:
    pattern = r"http+s?:\/\/[a-z0-9.]*\.[a-z]*+\/?"
    return bool(re.fullmatch(pattern, domain))


"""
write tests for is_http_domain function
"""


def test_https():
    assert is_http_domain("https://wikipedia.org")


def test_http():
    assert is_http_domain("http://wikipedia.org")


def test_slash_at_the_end():
    assert is_http_domain("https://wikipedia.org/")


def test_invalid():
    assert is_http_domain("griddynamics.com") == False
