from utilities.storage import read_data

DIGITS = [str(digit) for digit in range(10)]


def plot(data, width, row, column, number):
    print(5 * '-', row, column, number)
    _rows = range(row - 1, row + 2)
    for _row in _rows:
        if _row < 0:
            print((2 + width) * '.')
            continue
        if _row > len(data) - 1:
            print((2 + width) * '.')
            continue
        _loc_col_start = column - 1 if column > 0 else column
        _loc_col_end = column + width + 1
        _line = data[_row][_loc_col_start:_loc_col_end]
        _line = ''.join(_line)
        if column == 0:
            _line = '.' + _line
        print(_line)


def get_symbol_positions(grid: list[list]) -> dict:
    symbols = {}
    for row, line in enumerate(grid):
        for column, character in enumerate(line):
            if character not in [*DIGITS, '.']:
                symbols[(row, column)] = character
    return symbols


def get_number_positions(grid: list[list]) -> dict:
    numbers = {}
    for row, line in enumerate(grid):
        digits = []
        for column, characters in enumerate(line):
            if characters not in [*DIGITS, '.']:
                if digits:
                    start = column - len(digits)
                    numbers[(row, start)] = int(''.join(digits))
                    digits = []
                continue

            digits.append(characters)
            if column == len(line) - 1:
                start = column - len(digits)
                numbers[(row, start)] = int(''.join(digits))
            continue
    return numbers


def get_points_of_interest(numbers: dict, symbols: dict) -> set:
    points_of_interest = set()
    for position, number in numbers.items():
        row, column = position
        width = len(str(number))
        for local_row in range(row - 1, row + 2):
            for local_column in range(column - 1, column + width + 1):
                local_position = (local_row, local_column)
                if local_position in symbols.keys():
                    points_of_interest.add(position)
    return points_of_interest


def get_numbers_of_interest(numbers: dict, positions: set) -> list:
    numbers_of_interest = []
    for position in positions:
        number = numbers[position]
        numbers_of_interest.append(number)
    return numbers_of_interest


def first_part(data: str) -> int:
    grid = [list(line) for line in data.splitlines()]
    numbers = get_number_positions(grid)
    symbols = get_symbol_positions(grid)
    points_of_interest = get_points_of_interest(numbers, symbols)
    numbers_of_interest = get_numbers_of_interest(numbers, points_of_interest)
    return sum(numbers_of_interest)


def second_part(data: str) -> int:
    grid = [list(line) for line in data.splitlines()]
    numbers = get_number_positions(grid)
    symbols = get_symbol_positions(grid)
    total = 0
    for position, symbol in symbols.items():
        local_row, local_column = position
        if symbol != '*':
            continue
        numbers_with_gears = set()
        for row in range(local_row - 1, local_row + 2):
            for column in range(local_column - 1, local_column + 2):
                value = data[row][column]
                if value in DIGITS:
                    columns = [c for r, c in numbers.keys() if r == row and c <= column]
                    col = sorted(columns)[-1]
                    numbers_with_gears.add((row, col))
        if len(numbers_with_gears) == 2:
            x = list(numbers_with_gears)
            product = numbers[x[0]] * numbers[x[1]]
            total += product
    return total


def main() -> None:
    data = read_data(2023, 3, 'prod.txt')

    first_answer = first_part(data)
    print(f"Part 1: {first_answer}")

    second_answer = second_part(data)
    print(f"Part 2: {second_answer}")
