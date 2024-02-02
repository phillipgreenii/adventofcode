import unittest

import support

import day15

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day15","example")
        result = day15.part1(input, 10)
        self.assertEqual(result, '26')

    def test_part2(self):
        input = support.load_example("day15","example")
        result = day15.part2(input, 0, 20)
        self.assertEqual(result, '56000011')

