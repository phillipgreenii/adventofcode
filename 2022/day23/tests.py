import unittest

import support

import day23

class Tests(unittest.TestCase):

    def test_part1_simple(self):
        input = support.load_example("day23","example-simple")
        result = day23.part1(input)
        self.assertEqual(result, '25')

    def test_part1(self):
        input = support.load_example("day23","example")
        result = day23.part1(input)
        self.assertEqual(result, '110')

    def test_part2(self):
        input = support.load_example("day23","example")
        result = day23.part2(input)
        self.assertEqual(result, '20')
