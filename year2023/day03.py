#! /usr/bin/env python3

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


def main() -> None:
    data = read_data(2023, 3, 'prod')
    data = [list(line) for line in data.splitlines()]

    numbers = {}
    symbols = {}
    for row, line in enumerate(data):
        digits = []
        for column, char in enumerate(line):
            if char in DIGITS:
                digits.append(char)
                if column == len(line) - 1:
                    start = column - len(digits)
                    numbers[(row, start)] = int(''.join(digits))
                continue
            else:
                if digits:
                    start = column - len(digits)
                    numbers[(row, start)] = int(''.join(digits))
                    digits = []
            if char == '.':
                continue
            else:
                symbols[(row, column)] = char
    # print(numbers)
    # print(symbols)

    points_of_interests = set()
    for pointer, number in numbers.items():
        row, column = pointer
        width = len(str(number))
        for local_row in range(row - 1, row + 2):
            for local_column in range(column - 1, column + width + 1):
                local_pointer = (local_row, local_column)
                if local_pointer in symbols.keys():
                    points_of_interests.add(pointer)
        # if pointer not in points_of_interests:
        #     plot(data, width, row, column, number)
    # print(points_of_interests)

    numbers_of_interest = []
    for pointer in points_of_interests:
        number = numbers[pointer]
        numbers_of_interest.append(number)
    # print(numbers_of_interest)

    print(f"Part 1: {sum(numbers_of_interest)}")

    total = 0
    for pointer, symbol in symbols.items():
        numbers_with_gears = set()
        local_row, local_column = pointer
        if symbol != '*':
            continue
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
    print(f"Part 2: {total}")


if __name__ == '__main__':
    main()
