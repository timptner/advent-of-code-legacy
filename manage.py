#! /usr/bin/env python3

import unittest

from argparse import ArgumentParser

from tests import year2023
from year2023 import day03, day04


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('command', choices=['test', 'solve'])
    parser.add_argument('year', type=int, choices=range(2015, 2024))
    parser.add_argument('day', type=int, choices=range(1, 26))

    args = parser.parse_args()
    year = args.year
    day = args.day

    if args.command == 'test':
        tests = {
            2023: {
                3: year2023.TestDay03,
                4: year2023.TestDay04,
            },
        }
        cls = tests[year][day]

        suite = unittest.TestSuite()
        result = unittest.TestResult()

        test_first_part = cls('test_first_part')
        test_second_part = cls('test_second_part')

        suite.addTests([test_first_part, test_second_part])
        suite.run(result=result)
        if not result.wasSuccessful():
            print("Tests failed!")
        else:
            print("Tests passed!")

    if args.command == 'solve':
        solutions = {
            2023: {
                3: day03,
                4: day04,
            },
        }
        func = solutions[year][day]
        func.main()


if __name__ == '__main__':
    main()
