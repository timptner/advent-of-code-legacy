#! /usr/bin/env python3

import unittest

from argparse import ArgumentParser
from datetime import date
from importlib import import_module

from utilities.backend import get_puzzle_input
from utilities.console import console
from utilities.decorators import measure_time
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
    console.print(f"Solving puzzle for year {args.year} day {args.day}")

    try:
        module = import_module(f'year{args.year}.day{args.day:02d}')
    except ModuleNotFoundError:
        console.print("Solution for this puzzle is missing", style='red')
        return

    for part in range(1, 3):
        console.print(f"Trying part {part}")
        if not args.skip_test:
            try:
                test_result = test(args.year, args.day, part)
            except ModuleNotFoundError:
                console.print("Test module for this year is missing", style='red')
                return
            except AttributeError:
                console.print("Test case for this puzzle is missing", style='red')
                return

            if not test_result.wasSuccessful():
                for test_case, failure in test_result.failures:
                    console.print(f"Test execution [red]failed")
                    console.print(failure)

                for test_case, error in test_result.errors:
                    console.print(error)
                    console.print(f"Run into an [red]error[/red] while running test")

                continue

            console.print("Test was [green]passed")
        func_parts = {
            1: module.first_part,
            2: module.second_part,
        }
        func = func_parts[part]
        data = get_puzzle_input(year=args.year, day=args.day)
        timed_func = measure_time(func)
        value = timed_func(data)
        console.print(f"Answer: {value}")


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

    parser_solve = subparsers.add_parser('solve', help="Solve puzzle for specific year and day")
    parser_solve.add_argument('--year', type=int, choices=range(2016, 2024), default=today.year, help="Year of event")
    parser_solve.add_argument('--day', type=int, choices=range(1, 26), default=today.day, help="Day of advent")
    parser_solve.add_argument('--skip-test', action='store_true')
    parser_solve.set_defaults(func=solve)

    parser_test = subparsers.add_parser('test', help="Test all available puzzle")
    parser_test.set_defaults(func=test_all)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
