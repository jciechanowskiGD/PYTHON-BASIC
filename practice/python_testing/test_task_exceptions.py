"""
Write tests for division() function in 2_python_part_2/task_exceptions.py
In case (1,1) it should check if exception were raised
In case (1,0) it should check if return value is None and "Division by 0" printed
If other cases it should check if division is correct

TIP: to test output of print() function use capfd fixture
https://stackoverflow.com/a/20507769
"""

from python_part_2.task_exceptions import division, DivisionByOneException
import pytest


def test_division_ok(capfd):
    assert division(2, 4) == 0.5


def test_division_by_zero(capfd):
    assert division(1, 0) == None
    captured = capfd.readouterr()
    assert captured.out.split("\n")[0] == "Division by 0"


def test_division_by_one(capfd):
    with pytest.raises(DivisionByOneException):
        division(1, 1)
