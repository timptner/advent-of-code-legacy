#! /usr/bin/env python3

import unittest

from argparse import ArgumentParser

import tests.year2023
import year2023.day04


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument('command', choices=['test', 'solve'])

    args = parser.parse_args()

    if args.command == 'test':
        suite = unittest.TestSuite()
        result = unittest.TestResult()

        test_first_part = tests.year2023.TestDay04('test_first_part')
        test_second_part = tests.year2023.TestDay04('test_second_part')

        suite.addTests([test_first_part, test_second_part])
        suite.run(result=result)
        if not result.wasSuccessful():
            print("Tests failed!")
        else:
            print("Tests passed!")

    if args.command == 'solve':
        year2023.day04.main()


if __name__ == '__main__':
    main()
