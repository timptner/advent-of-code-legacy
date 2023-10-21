#! /usr/bin/env python3

from utilities.storage import read_data


def get_sections(sections: str) -> set:
    first, last = sections.split('-')
    first = int(first)
    last = int(last)
    sections = set(range(first, last + 1))
    return sections


def get_pairs() -> list:
    data = read_data(year=2022, day=4)
    pairs = []
    for line in data.splitlines():
        elv1, elv2 = line.split(',')
        sections1 = get_sections(elv1)
        sections2 = get_sections(elv2)
        pair = (sections1, sections2)
        pairs.append(pair)
    return pairs


def get_amount_fully_contained() -> int:
    counter = 0
    for pair in get_pairs():
        a, b = pair
        if (a <= b) or (b <= a):
            counter += 1

    return counter


def get_amount_partly_contained() -> int:
    counter = 0
    for pair in get_pairs():
        a, b = pair
        if a & b:
            counter += 1

    return counter


def main() -> None:
    amount_fully = get_amount_fully_contained()
    print(f"Part 1: {amount_fully}")

    amount_partly = get_amount_partly_contained()
    print(f"Part 2: {amount_partly}")


if __name__ == '__main__':
    main()
