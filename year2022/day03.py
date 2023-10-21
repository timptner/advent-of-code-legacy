#! /usr/bin/env python3

import string

from utilities.storage import read_data


def get_rucksacks() -> list:
	data = read_data(year=2022, day=3)
	rucksacks = []
	for rucksack in data.splitlines():
		rucksacks.append(rucksack)
	return rucksacks


def get_rucksacks_grouped() -> list:
	rucksacks_grouped = []
	group = []
	for rucksack in get_rucksacks():
		group.append(rucksack)
		if len(group) > 2:
			rucksacks_grouped.append(group)
			group = []
	return rucksacks_grouped


def compare(a: str, b: str) -> list:
	matches = []
	for letter in a:
		if letter in list(b):
			if letter in matches:
				continue
			matches.append(letter)
	return matches


LETTERS = string.ascii_letters
NUMBERS = range(1, len(LETTERS) + 1)
CONVERTER = dict(zip(LETTERS, NUMBERS))


def get_priority(letter: str) -> int:
	try:
		priority = CONVERTER[letter]
	except KeyError:
		raise ValueError("Letter has no priority.")

	return priority


def get_single_priority(items1: str, items2: str) -> int:
	duplicated_items = compare(items1, items2)
	if len(duplicated_items) != 1:
		raise AssertionError("Only 1 item should be contained in both compartments.")
	priority = get_priority(duplicated_items[0])
	return priority


def get_priority_sum() -> int:
	priority_sum = 0
	for rucksack in get_rucksacks():
		compartment_size = int(len(rucksack) / 2)
		items1 = rucksack[:compartment_size]
		items2 = rucksack[compartment_size:]
		priority_sum += get_single_priority(items1, items2)
	return priority_sum


def get_priority_sum_grouped() -> int:
	priority_sum_grouped = 0
	for group in get_rucksacks_grouped():
		items1 = compare(group[0], group[1])
		items2 = compare(group[1], group[2])
		items1 = ''.join(items1)
		items2 = ''.join(items2)
		priority_sum_grouped += get_single_priority(items1, items2)
	return priority_sum_grouped


def main() -> None:
	priority_sum = get_priority_sum()
	print(f"Part 1: {priority_sum}")

	priority_sum_grouped = get_priority_sum_grouped()
	print(f"Part 2: {priority_sum_grouped}")


if __name__ == '__main__':
	main()
