import time

import numpy as np

Rule = tuple[range, range]  # source, destination


class Category:
    def __init__(self, rules: list[Rule]) -> None:
        self.rules = rules

    def get_destination(self, value: int) -> int:
        for source, destination in self.rules:
            if value in source:
                index = source.index(value)
                return destination[index]
        return value

    def get_source(self, value: int) -> int:
        for source, destination in self.rules:
            if value in destination:
                index = destination.index(value)
                return source[index]
        return value


Seed = int


def parse_input(data: str) -> tuple[list[Seed], dict[str, Category]]:
    groups = data.split('\n\n')

    seeds = groups.pop(0)
    seeds = [int(seed) for seed in seeds.removeprefix('seeds: ').split()]

    categories = {}
    for group in groups:
        lines = group.splitlines()

        title = lines.pop(0).removesuffix(' map:')

        rules: list[Rule] = []
        for line in lines:
            destination_start, source_start, length = [int(number) for number in line.split()]
            rule = (
                range(source_start, source_start + length),
                range(destination_start, destination_start + length),
            )
            rules.append(rule)
        category = Category(rules)
        categories[title] = category

    return seeds, categories


def get_seed(categories: dict[str, Category], value: int) -> int:
    order = [
        'seed-to-soil',
        'soil-to-fertilizer',
        'fertilizer-to-water',
        'water-to-light',
        'light-to-temperature',
        'temperature-to-humidity',
        'humidity-to-location',
    ]
    for title in reversed(order):
        category = categories[title]
        value = category.get_source(value)
    return value


def first_part(data: str) -> int:
    seeds, categories = parse_input(data)

    print("Start loop")
    timer = time.time()
    for number in range(np.iinfo(np.uint64).max):
        now = time.time()
        if now - timer > 10:
            print(number)
            timer = now
        seed = get_seed(categories, number)
        if seed in seeds:
            print(number)
            return number


def second_part(data: str) -> int:
    seeds, categories = parse_input(data)

    seed_ranges = []
    for index in range(0, len(seeds), 2):
        start = seeds[index]
        length = seeds[index + 1]
        seed_range = range(start, start + length)
        seed_ranges.append(seed_range)

    print("Start loop")
    timer = time.time()
    for number in range(np.iinfo(np.uint64).max):
        now = time.time()
        if now - timer > 10:
            print(number)
            timer = now
        seed = get_seed(categories, number)
        for seed_range in seed_ranges:
            if seed in seed_range:
                print(number)
                return number
