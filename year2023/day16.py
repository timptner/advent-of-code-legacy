import sys

from enum import Enum
from typing import TypeAlias

from utilities.backend import BasePuzzle
from utilities.models import Grid

sys.setrecursionlimit(5000)


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


Point: TypeAlias = tuple[int, int]


class Layout(Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.energized_points = {}

    def get_next(self, point: Point, direction: Direction) -> None:
        row, column = point
        rows, columns = self.size
        if row < 0 or row > rows - 1 or column < 0 or column > columns - 1:
            return

        if point in self.energized_points.keys():
            if direction in self.energized_points[point]:
                return
            else:
                directions = self.energized_points[point]
                directions.add(direction)
        else:
            self.energized_points[point] = {direction}

        symbol = self[point]
        if symbol == '\\':
            if direction == Direction.NORTH:
                next_direction = Direction.WEST
                next_point = row, column - 1
                self.get_next(next_point, next_direction)
            elif direction == Direction.EAST:
                next_direction = Direction.SOUTH
                next_point = row + 1, column
                self.get_next(next_point, next_direction)
            elif direction == Direction.SOUTH:
                next_direction = Direction.EAST
                next_point = row, column + 1
                self.get_next(next_point, next_direction)
            elif direction == Direction.WEST:
                next_direction = Direction.NORTH
                next_point = row - 1, column
                self.get_next(next_point, next_direction)
            else:
                raise ValueError(f"Unknown direction '{direction}'")
        elif symbol == '/':
            if direction == Direction.NORTH:
                next_direction = Direction.EAST
                next_point = row, column + 1
                self.get_next(next_point, next_direction)
            elif direction == Direction.EAST:
                next_direction = Direction.NORTH
                next_point = row - 1, column
                self.get_next(next_point, next_direction)
            elif direction == Direction.SOUTH:
                next_direction = Direction.WEST
                next_point = row, column - 1
                self.get_next(next_point, next_direction)
            elif direction == Direction.WEST:
                next_direction = Direction.SOUTH
                next_point = row + 1, column
                self.get_next(next_point, next_direction)
            else:
                raise ValueError(f"Unknown direction '{direction}'")
        elif symbol == '-':
            if direction == Direction.NORTH:
                next_direction = Direction.EAST
                next_point = row, column + 1
                self.get_next(next_point, next_direction)
                next_direction = Direction.WEST
                next_point = row, column - 1
                self.get_next(next_point, next_direction)
            elif direction == Direction.EAST:
                next_direction = direction
                next_point = row, column + 1
                self.get_next(next_point, next_direction)
            elif direction == Direction.SOUTH:
                next_direction = Direction.EAST
                next_point = row, column + 1
                self.get_next(next_point, next_direction)
                next_direction = Direction.WEST
                next_point = row, column - 1
                self.get_next(next_point, next_direction)
            elif direction == Direction.WEST:
                next_direction = Direction.WEST
                next_point = row, column - 1
                self.get_next(next_point, next_direction)
            else:
                raise ValueError(f"Unknown direction '{direction}'")
        elif symbol == '|':
            if direction == Direction.NORTH:
                next_direction = Direction.NORTH
                next_point = row - 1, column
                self.get_next(next_point, next_direction)
            elif direction == Direction.EAST:
                next_direction = Direction.NORTH
                next_point = row - 1, column
                self.get_next(next_point, next_direction)
                next_direction = Direction.SOUTH
                next_point = row + 1, column
                self.get_next(next_point, next_direction)
            elif direction == Direction.SOUTH:
                next_direction = Direction.SOUTH
                next_point = row + 1, column
                self.get_next(next_point, next_direction)
            elif direction == Direction.WEST:
                next_direction = Direction.NORTH
                next_point = row - 1, column
                self.get_next(next_point, next_direction)
                next_direction = Direction.SOUTH
                next_point = row + 1, column
                self.get_next(next_point, next_direction)
            else:
                raise ValueError(f"Unknown direction '{direction}'")
        elif symbol == '.':
            next_direction = direction
            if direction == Direction.NORTH:
                next_point = row - 1, column
                self.get_next(next_point, next_direction)
            elif direction == Direction.EAST:
                next_point = row, column + 1
                self.get_next(next_point, next_direction)
            elif direction == Direction.SOUTH:
                next_point = row + 1, column
                self.get_next(next_point, next_direction)
            elif direction == Direction.WEST:
                next_point = row, column - 1
                self.get_next(next_point, next_direction)
            else:
                raise ValueError(f"Unknown direction '{direction}'")
        else:
            raise ValueError(f"Unknown symbol '{symbol}'")


class Puzzle(BasePuzzle):
    year = 2023
    day = 16
    name = "The Floor Will Be Lava"

    def part1(self, text: str) -> int:
        layout = Layout(text)

        start_point = (0, 0)
        layout.get_next(start_point, Direction.EAST)

        # rows, columns = layout.size
        # for row in range(rows):
        #     line = []
        #     for column in range(columns):
        #         point = row, column
        #         if point in layout.energized_points:
        #             line.append('#')
        #         else:
        #             line.append('.')
        #     print(''.join(line))

        return len(layout.energized_points.keys())

    def part2(self, text: str) -> int:
        layout = Layout(text)

        rows, columns = layout.size
        start_positions = [[(row, 0), Direction.EAST] for row in range(rows)]
        start_positions += [[(row, columns - 1), Direction.WEST] for row in range(rows)]
        start_positions += [[(0, column), Direction.SOUTH] for column in range(columns)]
        start_positions += [[(rows - 1, column), Direction.NORTH] for column in range(columns)]

        results = {}
        for point, direction in start_positions:
            layout.energized_points = {}
            layout.get_next(point, direction)
            results[point, direction] = len(layout.energized_points.keys())

        return max(results.values())

    @property
    def test_data(self) -> dict:
        text = r"""
        .|...\....
        |.-.\.....
        .....|-...
        ........|.
        ..........
        .........\
        ..../.\\..
        .-.-/..|..
        .|....-|.\
        ..//.|....
        """

        return {
            'part1': (text, 46),
            'part2': (text, 51),
        }
