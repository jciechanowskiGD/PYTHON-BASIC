"""
Write function which receives line of space sepparated words.
Remove all duplicated words from line.
Restriction:
Examples:
    >>> remove_duplicated_words('cat cat dog 1 dog 2')
    'cat dog 1 2'
    >>> remove_duplicated_words('cat cat cat')
    'cat'
    >>> remove_duplicated_words('1 2 3')
    '1 2 3'
"""


def remove_duplicated_words(line: str) -> str:
    # if order isnt important
    # res = set(line.split())

    # if order is important
    res = []
    for word in line.split():
        if word not in res:
            res.append(word)
    return res


print(remove_duplicated_words("cat cat dog 1 dog 2"))
