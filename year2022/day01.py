#! /usr/bin/env python3

from utilities.storage import read_data


def get_cargos() -> list:
    data = read_data(year=2022, day=1)
    elves = data.split('\n\n')

    cargos = []
    for elv in elves:
        cargo = [int(meal) for meal in elv.split('\n')]
        cargos.append(sum(cargo))

    return cargos


def get_max_calories() -> int:
    cargos = get_cargos()
    max_calories = max(cargos)
    return max_calories


def get_top3_calories_total() -> int:
    cargos = get_cargos()
    top3_calories = sorted(cargos, reverse=True)[:3]
    top3_calories_total = sum(top3_calories)
    return top3_calories_total


def main() -> None:
    max_calories = get_max_calories()
    print(f"Part 1: {max_calories}")

    top3_calories_total = get_top3_calories_total()
    print(f"Part 2: {top3_calories_total}")


if __name__ == '__main__':
    main()
