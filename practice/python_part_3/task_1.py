"""
using datetime module find number of days from custom date to now
Custom date is a string with format "2021-12-24"
If entered string pattern does not match, raise a custom Exception
If entered date is from future, return negative value for number of days
    >>> calculate_days('2021-10-07')  # for this example today is 6 october 2021
    -1
    >>> calculate_days('2021-10-05')
    1
    >>> calculate_days('10-07-2021')
    WrongFormatException
"""

from datetime import datetime
from freezegun import freeze_time
import pytest


class WrongFormatException(Exception):
    pass


def calculate_days(from_date: str) -> int:
    format = "%Y-%m-%d"
    try:
        datetime.strptime(from_date, format)
    except ValueError as e:
        raise WrongFormatException("Wrong date format")

    difference = datetime.today() - datetime.fromisoformat(from_date)
    return difference.days


"""
Write tests for calculate_days function
Note that all tests should pass regardless of the day test was run
Tip: for mocking datetime.now() use https://pypi.org/project/pytest-freezegun/
"""

# I use python 3.12 and pytest-freezegun dont work here bc distutils module was deprecated and rm
# I used freezegun from https://pypi.org/project/freezegun/


@freeze_time("2025-06-13")
def test_negative_days():
    assert calculate_days("2025-06-16") == -3


@freeze_time("2025-06-13")
def test_todays_date():
    assert calculate_days("2025-06-13") == 0


@freeze_time("2025-06-13")
def test_positive_days():
    assert calculate_days("2025-06-10") == 3


@freeze_time("2025-06-13")
def test_month_before_date():
    assert calculate_days("2025-05-13") == 31


@freeze_time("2025-06-13")
def test_bad_format():
    with pytest.raises(WrongFormatException):
        calculate_days("2025-13-01")
