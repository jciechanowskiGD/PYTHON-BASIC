"""
Write function which reads a number from input nth times.
If an entered value isn't a number, ignore it.
After all inputs are entered, calculate an average entered number.
Return string with following format:
If average exists, return: "Avg: X", where X is avg value which rounded to 2 places after the decimal
If it doesn't exists, return: "No numbers entered"
Examples:
    user enters: 1, 2, hello, 2, world
    >>> read_numbers(5)
    Avg: 1.67
    ------------
    user enters: hello, world, foo, bar, baz
    >>> read_numbers(5)
    No numbers entered

"""


def read_numbers(n: int) -> str:
    nums = []
    for _ in range(n):
        inp = input('user enters: ')
        if inp and inp.isnumeric(): # thats potential weak point, I dont know if float covers complex numbers
            nums.append(float(inp))
    if not nums:
        return 'No numbers entered'

    return f'Avg: {sum(nums)/len(nums)}'

if __name__ == "__main__":
    print(read_numbers(5))

