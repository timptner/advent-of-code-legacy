import logging
import os
import sys

from abc import abstractmethod
from pathlib import Path
from typing import Union
from urllib.parse import urljoin

import requests

from utilities.decorators import cache, rate_limit, measure_time
from utilities.format import human_delta

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


def trim(text: str) -> str:
    lines = text.expandtabs().splitlines()

    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))

    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())

    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)

    return '\n'.join(trimmed)


class BasePuzzle:
    def __init__(self, *args, **kwargs):
        padding = '-' * 10
        logger.info(f"{padding} {self.name} ({self.year}/{self.day}) {padding}")

    @property
    @abstractmethod
    def year(self) -> int:
        pass

    @property
    @abstractmethod
    def day(self) -> int:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def test_data(self) -> dict:
        pass

    def get_test_data(self, part) -> tuple[str, int]:
        text, value = self.test_data[f'part{part}']
        return trim(text), value

    def get_input_data(self) -> str:
        text = get_puzzle_input(year=self.year, day=self.day)
        return text

    @abstractmethod
    def part1(self, text: str) -> int:
        pass

    @measure_time
    def part1_timed(self, text: str) -> int:
        return self.part1(text)

    @abstractmethod
    def part2(self, text: str) -> int:
        pass

    @measure_time
    def part2_timed(self, text: str) -> int:
        return self.part2(text)

    def get_solver(self, part: int, timer: bool = False) -> Union[part1, part2, part1_timed, part2_timed]:
        choices = (1, 2)
        if part not in choices:
            raise ValueError(f"Valid options: {choices}")

        if timer:
            solver = getattr(self, f'part{part}_timed')
        else:
            solver = getattr(self, f'part{part}')

        return solver

    def test(self, part: int) -> None:
        text, value = self.get_test_data(part)
        solver = self.get_solver(part)
        solution = solver(text)
        assert solution == value, f"Test for part {part} [red]failed[/red] ({solution} != {value})"
        logger.info(f"Test for part {part} [green]passed")

    def solve(self, part: int) -> None:
        logger.info(f"--- Part {part}")
        self.test(part)

        text = self.get_input_data()
        solver = self.get_solver(part, timer=True)
        value, delta = solver(text)
        logger.info(f"Solution for part {part}: {value}")
        logger.info(f"Time spent: {human_delta(delta)}")
