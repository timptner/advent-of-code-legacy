import logging
import os

from pathlib import Path
from urllib.parse import urljoin

import requests

from utilities.decorators import cache, rate_limit, measure_time

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent

ENDPOINT = 'https://adventofcode.com'


@cache
@rate_limit(seconds=900)
def get_puzzle_input(*, year: int, day: int) -> str:
    url = urljoin(ENDPOINT, f'{year}/day/{day}/input')
    session = os.environ['AOC_SESSION']
    headers = {
        'Cookie': f'session={session}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"[{response.status_code}] {response.content}")

    logger.info("Retrieved puzzle input from backend")
    return response.content.decode('utf-8')


def remove_indentation(text: str) -> str:
    lines = text.splitlines()
    length = len(lines[-1])
    lines = [line.removeprefix(' ' * length) for line in lines]
    text = '\n'.join(lines)
    return text


class BasePuzzle:
    year = None
    day = None
    name = None

    test_data = {}

    def __init__(self) -> None:
        if self.year is None:
            raise NotImplementedError("Please specify year attribute")
        if self.day is None:
            raise NotImplementedError("Please specify day attribute")
        if self.name is None:
            raise NotImplementedError("Please specify name attribute")

        self.update_test_data()
        for part, data in self.test_data.items():
            text, value = data
            self.test_data[part] = (remove_indentation(text).strip(), value)

        self.input_data = get_puzzle_input(year=self.year, day=self.day)

    def part1(self, text: str) -> int:
        raise NotImplementedError("Please overwrite function for first part")

    def part2(self, text: str) -> int:
        raise NotImplementedError("Please overwrite function for second part")

    def update_test_data(self) -> None:
        raise NotImplementedError("Please overwrite function for test input")

    def _test_part(self, part: int) -> None:
        text, value = self.test_data[f'part{part}']
        func = getattr(self, f'part{part}')
        answer = func(text)
        assert answer == value, f"Test for part {part} [red]failed[/red] ({answer} != {value})"
        logger.info(f"Test for part {part} [green]passed")

    def _solve_part(self, part: int) -> None:
        text = self.input_data
        func = getattr(self, f'part{part}')
        func = measure_time(func)
        value = func(text)
        logger.info(f"Solution for part {part}: {value}")

    def solve(self) -> None:
        padding = '-' * 10
        logger.info(f"{padding} {self.name} ({self.year}/{self.day}) {padding}")

        logger.info("--- Part 1")
        self._test_part(1)
        self._solve_part(1)

        logger.info("--- Part 2")
        self._test_part(2)
        self._solve_part(2)
