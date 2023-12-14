from enum import IntEnum

from utilities.backend import BasePuzzle
from utilities.models import Grid


class Orientation(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


class Dish(Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = Orientation.NORTH

    def rotate_left(self) -> None:
        super().rotate_left()
        try:
            next_orientation = Orientation(self.orientation.value + 1)
        except ValueError:
            next_orientation = Orientation.NORTH
        self.orientation = next_orientation

    def rotate_right(self) -> None:
        super().rotate_right()
        try:
            next_orientation = Orientation(self.orientation.value - 1)
        except ValueError:
            next_orientation = Orientation.WEST
        self.orientation = next_orientation

    def tilt(self) -> None:
        rows, columns = self.size

        lists_of_items = []
        for row in range(rows):
            items = [self[row, column] for column in range(columns)]
            lists_of_items.append(items)

        tilted_lines = []
        for list_of_items in zip(*lists_of_items):
            line = ''.join(list_of_items)
            parts = line.split('#')
            tilted_parts = []
            for part in parts:
                width = len(part)
                stones = part.replace('.', '')
                part = f"{stones:.<{width}s}"
                tilted_parts.append(part)
            tilted_line = '#'.join(tilted_parts)
            tilted_lines.append(list(tilted_line))

        data = {}
        for row, line in enumerate(zip(*tilted_lines)):
            for column, character in enumerate(line):
                data[row, column] = character
        self.data = data

    def cycle(self) -> None:
        for n in range(4):
            self.tilt()
            self.rotate_right()

    def get_load(self) -> int:
        while self.orientation != Orientation.NORTH:
            self.rotate_right()
        rows, columns = self.size
        load = 0
        for row in range(rows):
            for column in range(columns):
                value = self[row, column]
                if value != 'O':
                    continue
                load += rows - row
        return load


class Puzzle(BasePuzzle):
    year = 2023
    day = 14
    name = "Parabolic Reflector Dish"

    def part1(self, text: str) -> int:
        dish = Dish(text)
        dish.tilt()
        return dish.get_load()

    def part2(self, text: str) -> int:
        dish = Dish(text)
        known_patterns = {}
        counter = 0
        while True:
            dish.cycle()
            counter += 1
            pattern = str(dish)
            if pattern in known_patterns.keys():
                start = known_patterns[pattern]
                end = counter
                print(f"Found loop! Pattern at cycle {end} is equal to pattern from cycle {start}")
                break
            known_patterns[pattern] = counter
        length = end - start
        remains = (10**9 - start) % length
        for n in range(remains):
            dish.cycle()
        return dish.get_load()

    def update_test_data(self) -> None:
        text = """
        O....#....
        O.OO#....#
        .....##...
        OO.#O....O
        .O.....O#.
        O.#..O.#.#
        ..O..#O..O
        .......O..
        #....###..
        #OO..#....
        """
        self.test_data = {
            'part1': (text, 136),
            'part2': (text, 64),
        }
