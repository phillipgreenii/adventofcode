import unittest

import support

import day04

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day04","example")
        result = day04.part1(input)
        self.assertEqual(result, '2')

    def test_part2(self):
        input = support.load_example("day04","example")
        result = day04.part2(input)
        self.assertEqual(result, '4')

