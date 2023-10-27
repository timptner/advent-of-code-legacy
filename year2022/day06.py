#! /usr/bin/env python3

from utilities.storage import read_data


def parse_message(message: str, unique_letters: int = 4) -> int:
    """Parse message and find marker."""
    letters = list(message)
    length = len(letters) - (unique_letters - 1)
    for index in range(length):
        group = letters[index:index + unique_letters]
        if len(set(group)) == unique_letters:
            return index + unique_letters


def handle_messages(length: int) -> list[int]:
    data = read_data(2022, 6)
    markers = []
    for line in data.splitlines():
        marker = parse_message(line, length)
        markers.append(marker)
    return markers


def main() -> None:
    markers = handle_messages(4)
    print(f"Part 1: {markers}")

    markers = handle_messages(14)
    print(f"Part 1: {markers}")


if __name__ == '__main__':
    main()
