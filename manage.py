#! /usr/bin/env python3

import logging
import unittest

from argparse import ArgumentParser
from datetime import date
from importlib import import_module
from pathlib import Path

from rich.logging import RichHandler

from utilities.console import console
from utilities.storage import load_dotenv

logger = logging.getLogger('root')
logger.addHandler(RichHandler(
    markup=True,
    show_time=False,
    show_level=False,
))
logger.setLevel(logging.DEBUG)


def login(args) -> None:
    raise NotImplementedError("WIP")


def test(year: int, day: int, part: int) -> unittest.TestResult:
    module = import_module(f'tests.year{year}')
    cls = getattr(module, f'TestDay{day:02d}')

    test_names = {
        1: 'test_first_part',
        2: 'test_second_part',
    }
    test_name = test_names[part]

    result = unittest.TestResult()

    test_func = cls(test_name)
    test_func.run(result=result)

    return result


def solve(args) -> None:
    name = args.module
    logger.info(f"Trying to load module '{name}'")

    try:
        module = import_module(name)
    except ModuleNotFoundError:
        logger.error("[red]Module does not exist")
        exit(1)

    try:
        puzzle = module.Puzzle()
    except AttributeError:
        logger.error("[red]Module does not contain a puzzle solution")
        exit(1)

    puzzle.solve()


def test_all(args) -> None:
    console.print(f"Year\tDay\tPart 1\tPart 2")
    for year in range(2016, 2024):
        for day in range(1, 26):
            parts = []
            for part in range(1, 3):
                try:
                    is_success = test(year, day, part)
                except ModuleNotFoundError:
                    parts.append("[blue]Skipped")
                    continue
                except AttributeError:
                    parts.append("[blue]Skipped")
                    continue
                if is_success:
                    parts.append("[green]Passed")
                else:
                    parts.append("[red]Failed")
            console.print(f"{year}\t{day:>3}\t{parts[0]}\t{parts[1]}")


def get_default_module() -> str:
    today = date.today()

    year = today.year
    month = today.month
    day = today.day

    if month == 12 and day < 26:
        module = f'year{year}.day{day}'
    elif month == 12:
        module = f'year{year}.day25'
    else:
        module = f'year{year - 1}.day25'
    return module


def read_arguments() -> None:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(title="Available commands")

    parser_login = subparsers.add_parser('login', help="Log in to Advent of Code")
    parser_login.set_defaults(func=login)

    parser_solve = subparsers.add_parser('solve', help="Solve specific puzzle")
    parser_solve.add_argument('--module', default=get_default_module(), help="Module containing puzzle solver")
    parser_solve.set_defaults(func=solve)

    parser_test = subparsers.add_parser('test', help="Test all available puzzle")
    parser_test.set_defaults(func=test_all)

    args = parser.parse_args()
    args.func(args)


def main() -> None:
    load_dotenv()
    read_arguments()


if __name__ == '__main__':
    main()
