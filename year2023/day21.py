from enum import Enum

import numpy as np
import matplotlib.pyplot as plt
from rich.progress import track

from utilities.backend import BasePuzzle
from utilities.models import Grid
from utilities.storage import BASE_DIR


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)


class Point:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column

    def __repr__(self) -> str:
        return f"Point({self.row}, {self.column})"

    def __eq__(self, other):
        return all([
            self.row == other.row,
            self.column == other.column,
        ])

    def __hash__(self) -> int:
        values = (self.row, self.column)
        return hash(values)

    def values(self) -> tuple[int, int]:
        return self.row, self.column

    def move(self, direction: Direction) -> 'Point':
        row, column = direction.value
        return Point(self.row + row, self.column + column)


class Garden(Grid):
    def find(self, value: str) -> set[Point]:
        points = set()
        for (row, column), tile in self.data.items():
            if tile == value:
                point = Point(row, column)
                points.add(point)
        return points

    def get_value(self, row: int, column: int) -> str:
        rows, columns = self.size
        if row not in range(0, rows):
            row = row % rows
        if column not in range(0, columns):
            column = column % columns
        return self.data[row, column]

    def get_next_points(self, points: set[Point]) -> set[Point]:
        next_points = set()
        for point in points:
            for direction in Direction:
                next_point = point.move(direction)
                value = self.get_value(*next_point.values())
                if value == '#':
                    continue
                next_points.add(next_point)
        return next_points


class Puzzle(BasePuzzle):
    year = 2023
    day = 21
    name = "Step Counter"

    @property
    def test_data(self) -> dict:
        text = """
        ...........
        .....###.#.
        .###.##..#.
        ..#.#...#..
        ....#.#....
        .##..S####.
        .##..#...#.
        .......##..
        .##.#.####.
        .##..##.##.
        ...........
        """
        return {
            'part1': (text, 16),
            'part2': (text, 16733044),
        }

    def part1(self, text: str) -> int:
        steps = 6 if len(text) < 150 else 64
        garden = Garden(text)
        points = garden.find('S')
        for n in range(steps):
            points = garden.get_next_points(points)
        return len(points)

    def part2(self, text: str) -> int:
        garden = Garden(text)
        points = garden.find('S')
        data = []
        for n in track(range(1, 501), description="Calculating points for polyfit..."):
            points = garden.get_next_points(points)
            data.append((n, len(points)))
        data = np.array(data)
        z = np.polyfit(data[:, 0], data[:, 1], 2)
        p = np.poly1d(z)

        steps = 5000 if len(text) < 150 else 26501365

        # file = BASE_DIR / 'data' / '2023' / 'images' / '21' / 'curve.png'
        # if not file.parent.exists():
        #     file.parent.mkdir()
        #
        # x = np.linspace(0, 27 * 10**6, 100)
        #
        # fig, ax = plt.subplots()
        #
        # ax.plot(x, p(x))
        # ax.plot(data)
        # ax.plot(steps, p(steps), 'r')
        #
        # fig.savefig(file)

        return round(p(steps))
