import unittest

import support

import day13

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day13","example")
        result = day13.part1(input)
        self.assertEqual(result, '13')

    def test_part2(self):
        input = support.load_example("day13","example")
        result = day13.part2(input)
        self.assertEqual(result, '140')

