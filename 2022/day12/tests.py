import unittest

import support

import day12

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day12","example")
        result = day12.part1(input)
        self.assertEqual(result, '31')

    def test_part2(self):
        input = support.load_example("day12","example")
        result = day12.part2(input)
        self.assertEqual(result, '29')

