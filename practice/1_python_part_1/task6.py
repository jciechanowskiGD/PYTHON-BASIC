"""
Write function which receives filename and reads file line by line and returns min and mix integer from file.
Restriction: filename always valid, each line of file contains valid integer value
Examples:
    # file contains following lines:
        10
        -2
        0
        34
    >>> get_min_max('filename')
    (-2, 34)

Hint:
To read file line-by-line you can use this:
with open(filename) as opened_file:
    for line in opened_file:
        ...
"""
from typing import Tuple


def get_min_max(filename: str) -> Tuple[int, int]:
    min_val = float('inf')
    max_val = float('-inf')
    with open(filename) as file:
        for line in file:
            val = int(line)
            if val > max_val:
                max_val = val
            # no elif bc this is important for first step
            if val < min_val:
                min_val = val
        return min_val, max_val
    
    # another method is adding all vals to list and then using min(), max() on it
print(get_min_max('test.txt'))