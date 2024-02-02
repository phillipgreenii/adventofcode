import unittest

import support

import day06

class Tests(unittest.TestCase):

    def test_part1_1(self):
        input = support.load_example("day06","example-1")
        result = day06.part1(input)
        self.assertEqual(result, '7')

    def test_part1_2(self):
        input = support.load_example("day06","example-2")
        result = day06.part1(input)
        self.assertEqual(result, '5')

    def test_part1_3(self):
        input = support.load_example("day06","example-3")
        result = day06.part1(input)
        self.assertEqual(result, '6')

    def test_part1_4(self):
        input = support.load_example("day06","example-4")
        result = day06.part1(input)
        self.assertEqual(result, '10')

    def test_part1_5(self):
        input = support.load_example("day06","example-5")
        result = day06.part1(input)
        self.assertEqual(result, '11')

    def test_part2_1(self):
        input = support.load_example("day06","example-1")
        result = day06.part2(input)
        self.assertEqual(result, '19')

    def test_part2_2(self):
        input = support.load_example("day06","example-2")
        result = day06.part2(input)
        self.assertEqual(result, '23')

    def test_part2_3(self):
        input = support.load_example("day06","example-3")
        result = day06.part2(input)
        self.assertEqual(result, '23')

    def test_part2_4(self):
        input = support.load_example("day06","example-4")
        result = day06.part2(input)
        self.assertEqual(result, '29')

    def test_part2_5(self):
        input = support.load_example("day06","example-5")
        result = day06.part2(input)
        self.assertEqual(result, '26')

