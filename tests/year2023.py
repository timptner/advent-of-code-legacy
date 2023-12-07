from unittest import TestCase

from year2023 import day01, day02, day03, day04, day05, day06, day07


class TestDay01(TestCase):
    def setUp(self) -> None:
        data1 = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
        self.data1 = data1.strip()
        data2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
        self.data2 = data2.strip()

    def test_first_part(self) -> None:
        answer = day01.first_part(self.data1)
        self.assertEqual(answer, 142)

    def test_second_part(self) -> None:
        answer = day01.second_part(self.data2)
        self.assertEqual(answer, 281)


class TestDay02(TestCase):
    def setUp(self) -> None:
        data = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
        self.data = data.strip()

    def test_first_part(self) -> None:
        answer = day02.first_part(self.data)
        self.assertEqual(answer, 8)

    def test_second_part(self) -> None:
        answer = day02.second_part(self.data)
        self.assertEqual(answer, 2286)


class TestDay03(TestCase):
    def setUp(self) -> None:
        data = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
        self.data = data.strip()

    def test_first_part(self) -> None:
        answer = day03.first_part(self.data)
        self.assertEqual(answer, 4361)

    def test_second_part(self) -> None:
        answer = day03.second_part(self.data)
        self.assertEqual(answer, 467835)


class TestDay04(TestCase):
    def setUp(self) -> None:
        data = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
        self.data = data.strip()

    def test_first_part(self) -> None:
        answer = day04.first_part(self.data)
        self.assertEqual(answer, 13)

    def test_second_part(self) -> None:
        answer = day04.second_part(self.data)
        self.assertEqual(answer, 30)


class TestDay05(TestCase):
    def setUp(self) -> None:
        data = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
        self.data = data.strip()

    def test_first_part(self) -> None:
        answer = day05.first_part(self.data)
        self.assertEqual(answer, 35)

    def test_second_part(self) -> None:
        answer = day05.second_part(self.data)
        self.assertEqual(answer, 46)


class TestDay06(TestCase):
    def setUp(self) -> None:
        data = """
Time:      7  15   30
Distance:  9  40  200
"""
        self.data = data.strip()

    def test_first_part(self) -> None:
        answer = day06.first_part(self.data)
        self.assertEqual(answer, 288)

    def test_second_part(self) -> None:
        answer = day06.second_part(self.data)
        self.assertEqual(answer, 71503)


class TestDay07(TestCase):
    def setUp(self) -> None:
        data = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
        self.data = data.strip()

    def test_first_part(self) -> None:
        value = day07.first_part(self.data)
        self.assertEqual(value, 6440)

    def test_second_part(self) -> None:
        value = day07.second_part(self.data)
        self.assertEqual(value, 5905)
