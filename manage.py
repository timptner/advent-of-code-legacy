#! /usr/bin/env python3

import time
import unittest

from argparse import ArgumentParser
from importlib import import_module

from utilities.storage import read_data


def add_default_args(parser: ArgumentParser) -> None:
    parser.add_argument('year', type=int, choices=range(2016, 2024), help="Year of event")
    parser.add_argument('day', type=int, choices=range(1, 26), help="Day of advent")


def measure_execution_time(func, *args, **kwargs) -> (int, float):
    start = time.time()
    answer = func(*args, **kwargs)
    stop = time.time()
    delta = stop - start
    return answer, delta


def get_human_delta(delta: float) -> str:
    if delta < 1:
        return f"{delta * 1e3:.3f} ms"
    else:
        return f"{delta:.3f} s"


def solve(args) -> None:
    try:
        module = import_module(f'year{args.year}.day{args.day:02d}')
    except ModuleNotFoundError:
        print(f"No solution for puzzle year {args.year} day {args.day}")
        exit()

    data = read_data(args.year, args.day, 'prod.txt')

    answer, delta = measure_execution_time(module.first_part, data=data)
    print(f"Part 1: {answer} ({get_human_delta(delta)})")

    answer, delta = measure_execution_time(module.second_part, data=data)
    print(f"Part 2: {answer} ({get_human_delta(delta)})")


def validate_test_result(result: unittest.TestResult, year: int, day: int, part: int) -> None:
    msg = f"Test for part {part} of year {year} day {day}"
    if result.wasSuccessful():
        print(f"{msg} was successful")
    else:
        for test_case, failure in result.failures:
            print(failure)
        for test_case, error in result.errors:
            print(error)
        print(f"{msg} failed")


def test(args) -> None:
    try:
        module = import_module(f'tests.year{args.year}')
    except ModuleNotFoundError:
        print(f"No tests for puzzle year {args.year}")
        exit()

    try:
        cls = getattr(module, f'TestDay{args.day:02d}')
    except AttributeError:
        print(f"No test case for puzzle year {args.year} day {args.day}")
        exit()

    result = unittest.TestResult()
    test_first_part = cls('test_first_part')
    test_first_part.run(result=result)
    validate_test_result(result, args.year, args.day, 1)

    result = unittest.TestResult()
    test_second_part = cls('test_second_part')
    test_second_part.run(result=result)
    validate_test_result(result, args.year, args.day, 2)


def main() -> None:
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(title="Available commands")

    parser_solve = subparsers.add_parser('solve', help="Solve the puzzle")
    add_default_args(parser_solve)
    parser_solve.set_defaults(func=solve)

    parser_test = subparsers.add_parser('test', help="Test the puzzle")
    add_default_args(parser_test)
    parser_test.set_defaults(func=test)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
