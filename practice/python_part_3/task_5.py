"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""

from typing import Tuple
from urllib.request import urlopen
from urllib.error import HTTPError

# I get ssl problem when trying to access any website thats why I use these libraries
import certifi
import ssl


def make_request(url: str) -> Tuple[int, str]:
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urlopen(url, context=ssl_context) as response:
        body = response.read()
        status_code = response.status
        return status_code, body


if __name__ == "__main__":
    print(make_request("https://www.google.com/")[0])

"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""
import pytest


def test_valid_site():
    assert make_request("https://www.google.com")[0] == 200


def test_invalid_site():
    with pytest.raises(HTTPError):
        make_request("https://www.google.com/asdfdfawfwfffssfffffassssadwads")
