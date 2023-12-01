from utilities import storage


def filter_digits(chars: list) -> list:
    digits = []
    for char in chars:
        try:
            digit = int(char)
        except ValueError:
            continue
        digits.append(digit)
    return digits


def combine_digits(tens, ones) -> int:
    number = tens * 10 + ones
    return number


def get_numbers(data: str) -> int:
    total = 0
    for line in data.splitlines():
        chars = list(line)
        digits = filter_digits(chars)
        total += combine_digits(digits[0], digits[-1])
    return total


def replace_written_number(text: str) -> int | None:
    numbers = [
        ('one', 1),
        ('two', 2),
        ('three', 3),
        ('four', 4),
        ('five', 5),
        ('six', 6),
        ('seven', 7),
        ('eight', 8),
        ('nine', 9),
    ]
    for key, value in numbers:
        query = text.replace(key, str(value))
        digits = filter_digits(list(query))
        if digits:
            return digits[0]


def get_numbers_ext(data: str) -> int:
    total = 0
    for line in data.splitlines():
        chars = len(line)
        digits = []
        for index in range(chars):
            # read from left
            text = line[:index + 1]
            digit = replace_written_number(text)
            if digit:
                digits.append(digit)
                break

        for index in range(chars):
            # read from right
            text = line[-(index + 1):]
            digit = replace_written_number(text)
            if digit:
                digits.append(digit)
                break

        number = combine_digits(*digits)
        total += number
    return total


def main() -> None:
    year = 2023
    day = 1

    data = storage.read_data(year, day, 'prod')
    total = get_numbers(data)
    print(f"Part 1: {total}")

    data = storage.read_data(year, day, 'prod')
    total = get_numbers_ext(data)
    print(f"Part 1: {total}")


if __name__ == '__main__':
    main()
