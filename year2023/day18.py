from __future__ import annotations

from enum import Enum

import matplotlib.pyplot as plt

from utilities.backend import BasePuzzle
from utilities.storage import BASE_DIR

IMAGE_DIR = BASE_DIR / 'data' / '2023' / 'images' / '18'

if not IMAGE_DIR.exists():
    IMAGE_DIR.mkdir(parents=True)


class Instruction:
    def __init__(self, direction: str, distance: int) -> None:
        self.direction = Direction(direction)
        self.distance = distance

    def __repr__(self) -> str:
        return f"Instruction({self.direction}, {self.distance})"

    def next_coordinate(self, x: int, y: int) -> tuple[int, int]:
        return self.direction.move(x, y, self.distance)


class Turn(Enum):
    LEFT = 'L'
    RIGHT = 'R'


class Direction(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'

    def move(self, x: int, y: int, distance: int = 1) -> tuple[int, int]:
        moves = {
            self.UP: (0, 1),
            self.DOWN: (0, -1),
            self.LEFT: (-1, 0),
            self.RIGHT: (1, 0),
        }
        offset_x, offset_y = [n * distance for n in moves[self]]
        return x + offset_x, y + offset_y


DIRECTION_TO_TURN = {
    (Direction.UP, Direction.LEFT): Turn.LEFT,
    (Direction.UP, Direction.RIGHT): Turn.RIGHT,
    (Direction.DOWN, Direction.RIGHT): Turn.LEFT,
    (Direction.DOWN, Direction.LEFT): Turn.RIGHT,
    (Direction.LEFT, Direction.DOWN): Turn.LEFT,
    (Direction.LEFT, Direction.UP): Turn.RIGHT,
    (Direction.RIGHT, Direction.UP): Turn.LEFT,
    (Direction.RIGHT, Direction.DOWN): Turn.RIGHT,
}

OPPOSITE_DIRECTIONS = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


class Point:
    def __init__(self, x: int, y: int, turn: Turn) -> None:
        self.x = x
        self.y = y
        self.turn = turn

    def __repr__(self) -> str:
        return f"Point({self.x}, {self.y})"


class Puzzle(BasePuzzle):
    year = 2023
    day = 18
    name = "Lavaduct Lagoon"

    @property
    def test_data(self) -> dict:
        text = """
        R 6 (#70c710)
        D 5 (#0dc571)
        L 2 (#5713f0)
        D 2 (#d2c081)
        R 2 (#59c680)
        D 2 (#411b91)
        L 5 (#8ceee2)
        U 2 (#caa173)
        L 1 (#1b58a2)
        U 2 (#caa171)
        R 2 (#7807d2)
        U 3 (#a77fa3)
        L 2 (#015232)
        U 2 (#7a21e3)
        """
        return {
            'part1': (text, 62),
            'part2': (text, 952408144115),
        }

    def part1(self, text: str) -> int:
        instructions = []
        for line in text.splitlines():
            direction, distance, color = line.split(' ')
            instruction = Instruction(direction, int(distance))
            instructions.append(instruction)

        points = self.get_points(instructions)
        area = self.calculate_area(points)

        self.save_as_plot(points, 'part1.png')

        return area

    def part2(self, text: str) -> int:
        instructions = []
        for line in text.splitlines():
            directions = ['R', 'D', 'L', 'U']
            direction, distance, color = line.split(' ')
            direction = int(color[-2:-1])
            direction = directions[direction]
            distance = int(color[2:-2], 16)
            instruction = Instruction(direction, distance)
            instructions.append(instruction)

        points = self.get_points(instructions)
        area = self.calculate_area(points)

        self.save_as_plot(points, 'part2.png')

        return area

    @staticmethod
    def get_points(instructions: list[Instruction]) -> list[Point]:
        turns = []
        for index in range(-1, len(instructions) - 1):
            direction = instructions[index].direction
            next_direction = instructions[index + 1].direction
            turn = DIRECTION_TO_TURN[direction, next_direction]
            turns.append(turn)

        turn = turns.pop(0)
        point = Point(0, 0, turn)
        points = [point]
        for instruction in instructions[:-1]:
            x, y = instruction.next_coordinate(point.x, point.y)
            turn = turns.pop(0)
            last_point = points[-1]
            if last_point.turn == Turn.RIGHT and turn == Turn.RIGHT:
                x, y = instruction.direction.move(x, y)
            elif last_point.turn == Turn.LEFT and turn == Turn.LEFT:
                x, y = OPPOSITE_DIRECTIONS[instruction.direction].move(x, y)
            else:
                pass
            point = Point(x, y, turn)
            points.append(point)

        x, y = zip(*[(point.x, point.y) for point in points])
        offset_x = abs(min(x)) if min(x) < 0 else 0
        offset_y = abs(min(y)) if min(y) < 0 else 0
        for point in points:
            point.x += offset_x
            point.y += offset_y

        return points

    @staticmethod
    def calculate_area(points: list[Point]) -> int:
        area = 0
        for index in range(1, len(points)):
            last_point = points[index - 1]
            point = points[index]
            if last_point.x == point.x:
                continue
            if last_point.x < point.x:
                area += last_point.y * (point.x - last_point.x)
            else:
                area -= last_point.y * (last_point.x - point.x)
            pass

        return area

    @staticmethod
    def save_as_plot(points: list[Point], name: str):
        fig, ax = plt.subplots(figsize=(8, 8))
        x, y = zip(*[(point.x, point.y) for point in points])
        ax.fill(x, y)
        fig.savefig(IMAGE_DIR / name)
