#! /usr/bin/env python3

from pathlib import Path

file = Path(__file__).parent / 'data_prod.txt'


def read_data() -> str:
    content = file.read_text().strip()
    return content


def main() -> None:
    data = read_data()
    elves = data.split('\n\n')
    calories = []
    for elv in elves:
        meals = [int(meal) for meal in elv.split('\n')]
        calories.append(sum(meals))
    max_calories = max(calories)
    print(f"Maximum: {max_calories}")
    sorted_calories = sorted(calories, reverse=True)[:3]
    print(f"Sum of Top3: {sum(sorted_calories)}")


if __name__ == '__main__':
    main()
