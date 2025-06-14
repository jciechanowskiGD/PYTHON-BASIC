"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
from faker import Faker


def print_name_address(args: argparse.Namespace) -> None:
    fake = Faker()
    if args.number < 0:
        print("Negative number given")
        return

    if not args.some_name and not args.fake_address:
        print("No key-provider pairs provided")
        return

    for i in range(args.number):
        d = {}
        if args.some_name:
            function = getattr(fake, args.some_name)
            d["some_name"] = function()
        if args.fake_address:
            function = getattr(fake, args.fake_address)
            d["fake_address"] = function()
        print(d)


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "number", type=int, help="positive number of generated instances"
    )
    parser.add_argument("--fake_address", help="generate fake address")
    parser.add_argument("--some_name", help="generate some name")
    print_name_address(parser.parse_args())


if __name__ == "__main__":
    parser()

"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""
from unittest.mock import Mock


def test_two_dicts(capfd):
    m = Mock()
    m.number = 2
    m.some_name = "name"
    m.fake_address = "address"
    print_name_address(m)
    captured = capfd.readouterr()

    assert (
        len(captured.out.split("\n")) == 3
    )  # because when we print in line 38 default end='\n' and it creates '' at the end of split('\n')


def test_no_fields_provided(capfd):
    m = Mock()
    m.number = 2
    m.some_name = None
    m.fake_address = None
    print_name_address(m)
    captured = capfd.readouterr()

    assert captured.out.split("\n")[0] == "No key-provider pairs provided"


def test_negative_number(capfd):
    m = Mock()
    m.number = -1
    m.some_name = "name"
    m.fake_address = "address"
    print_name_address(m)
    captured = capfd.readouterr()

    assert captured.out.split("\n")[0] == "Negative number given"


def test_address(capfd):
    m = Mock()
    m.number = 2
    m.some_name = None
    m.fake_address = "address"
    print_name_address(m)
    captured = capfd.readouterr()
    assert captured.out.split("\n")[0].startswith("{'fake_address':")


def test_name(capfd):
    m = Mock()
    m.number = 2
    m.some_name = "name"
    m.fake_address = None
    print_name_address(m)
    captured = capfd.readouterr()
    assert captured.out.split("\n")[0].startswith("{'some_name':")
