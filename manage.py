#! /usr/bin/env python3

import unittest

from argparse import ArgumentParser
from datetime import date
from importlib import import_module
from pathlib import Path

from utilities.console import console
from utilities.storage import load_dotenv


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
    module_path: Path = args.module
    if not module_path.exists():
        raise FileNotFoundError("Module with puzzle solution does not exist")

    module_name = str(module_path).removesuffix('.py').replace('/', '.')

    try:
        module = import_module(module_name)
    except ModuleNotFoundError:
        print("Solution for this puzzle is missing")
        return

    puzzle = module.Puzzle()
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


def main() -> None:
    load_dotenv()
    today = date.today()

    parser = ArgumentParser()

    subparsers = parser.add_subparsers(title="Available commands")

    parser_solve = subparsers.add_parser('solve', help="Solve specific puzzle")
    parser_solve.add_argument('module', type=Path, default=f'year{today.year}/day{today.day:02d}.py', help="Path to module containing puzzle")
    parser_solve.set_defaults(func=solve)

    parser_test = subparsers.add_parser('test', help="Test all available puzzle")
    parser_test.set_defaults(func=test_all)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
