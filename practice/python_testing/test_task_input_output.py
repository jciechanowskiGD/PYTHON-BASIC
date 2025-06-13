"""
Write tests for a read_numbers function.
It should check successful and failed cases
for example:
Test if user inputs: 1, 2, 3, 4
Test if user inputs: 1, 2, Text

Tip: for passing custom values to the input() function
Use unittest.mock patch function
https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch

TIP: for testing builtin input() function create another function which return input() and mock returned value
"""

from unittest.mock import patch
from python_part_2.task_input_output import read_numbers, get_input


@patch("python_part_2.task_input_output.get_input", side_effect=["1", "2", "3", "4"])
def test_read_numbers_without_text_input(input):
    assert read_numbers(4) == "Avg: 2.5"


@patch("python_part_2.task_input_output.get_input", side_effect=["1", "2", "Text"])
def test_read_numbers_with_text_input(input):
    assert read_numbers(3) == "Avg: 1.5"


@patch(
    "python_part_2.task_input_output.get_input", side_effect=["Text", "Text", "Text"]
)
def test_read_numbers_with_only_text_input(input):
    assert read_numbers(3) == "No numbers entered"
