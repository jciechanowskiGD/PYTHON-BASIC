"""
Write function which executes custom operation from math module
for given arguments.
Restrition: math function could take 1 or 2 arguments
If given operation does not exists, raise OperationNotFoundException
Examples:
     >>> math_calculate('log', 1024, 2)
     10.0
     >>> math_calculate('ceil', 10.7)
     11
"""

import math
import pytest


class OperationNotFoundException(Exception):
    pass


# Do I have to validate *args?
def math_calculate(function: str, *args):
    if len(args) not in (1, 2):
        return

    not_dunder = [func for func in dir(math) if func[0] != "_"]

    if function not in not_dunder:
        raise OperationNotFoundException("Operation does not exist")

    func = getattr(math, function)

    return func(*args)


"""
Write tests for math_calculate function
"""


def test_log():
    assert math_calculate("log", 1024, 2) == 10.0


def test_ceil():
    assert math_calculate("ceil", 10.1) == 11


def test_exception():
    with pytest.raises(OperationNotFoundException):
        math_calculate("ggg", 1, 1)


def test_invalid_num_of_args():
    assert math_calculate("log", 10, 10, 10) is None
