#! /usr/bin/env python3

import string

from pathlib import Path

FILE = Path(__file__).parent / 'data_prod.txt'


def read_data() -> str:
	content = FILE.read_text().strip()
	return content


def compare(a: str, b: str) -> list:
	matches = []
	for letter in a:
		if letter in list(b):
			matches.append(letter)
	return matches


LETTERS = string.ascii_letters
NUMBERS = range(1, len(LETTERS) + 1)
CONVERTER = dict(zip(LETTERS, NUMBERS))


def main() -> None:
	data = read_data()
	total = 0
	for rucksack in data.splitlines():
		items = len(rucksack)
		half = int(items / 2)
		left = rucksack[:half]
		right = rucksack[half:]
		item = compare(left, right)[0]
		total += CONVERTER[item]
	print(f"Gesamt: {total}")

	groups = []
	group = []
	for rucksack in data.splitlines():
		group.append(rucksack)
		if len(group) == 3:
			groups.append(group)
			group = []
	total = 0
	for group in groups:
		letters = [
			''.join(compare(group[0], group[1])),
			''.join(compare(group[1], group[2])),
		]
		letter = compare(letters[0], letters[1])[0]
		total += CONVERTER[letter]
	print(f"Gesamt Pt2: {total}")


if __name__ == '__main__':
	main()
