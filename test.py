#! /usr/bin/env python3

import os
import unittest

from year2022.day01 import get_max_calories, get_top3_calories_total
from year2022.day02 import get_score
from year2022.day03 import get_priority_sum, get_priority_sum_grouped
from year2022.day04 import get_amount_fully_contained, get_amount_partly_contained


class TestYear2022(unittest.TestCase):
    def test_day01(self):
        self.assertEqual(get_max_calories(), 24000)
        self.assertEqual(get_top3_calories_total(), 45000)

    def test_day02(self):
        self.assertEqual(get_score(version=1)[1], 15)
        self.assertEqual(get_score(version=2)[1], 12)

    def test_day03(self):
        self.assertEqual(get_priority_sum(), 157)
        self.assertEqual(get_priority_sum_grouped(), 70)

    def test_day04(self):
        self.assertEqual(get_amount_fully_contained(), 2)
        self.assertEqual(get_amount_partly_contained(), 4)


if __name__ == '__main__':
    os.environ['AOC_ENV'] = 'test'
    unittest.main()
