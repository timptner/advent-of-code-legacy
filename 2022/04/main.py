#! /usr/bin/env python3

from pathlib import Path

file = Path(__file__).parent / 'data_prod.txt'


def read_data() -> str:
    content = file.read_text().strip()
    return content


def check_include(lower1, upper1, lower2, upper2) -> int:
    answer = 0
    if lower1 <= lower2 <= upper1:
        answer += 1
    if lower1 <= upper2 <= upper1:
        answer += 2
    if lower2 <= lower1 <= upper2:
        answer += 4
    if lower2 <= upper1 <= upper2:
        answer += 8
    return answer


def main() -> None:
    data = read_data()
    counter_part = 0
    counter_full = 0
    for pair in data.splitlines():
        elv1, elv2 = pair.split(',')
        lower1, upper1 = elv1.split('-')
        lower2, upper2 = elv2.split('-')
        answer = check_include(int(lower1), int(upper1), int(lower2), int(upper2))
        if answer == 0:
            continue
        elif answer in [3, 7, 11, 12, 13, 14, 15]:
            counter_full += 1
            counter_part += 1
        else:
            counter_part += 1

    print(f"Part 1: {counter_full}")
    print(f"Part 2: {counter_part}")


if __name__ == '__main__':
    main()
