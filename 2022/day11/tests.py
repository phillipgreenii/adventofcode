import unittest

import support

import day11

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day11","example")
        result = day11.part1(input)
        self.assertEqual(result, '10605')

    def test_part2(self):
        input = support.load_example("day11","example")
        result = day11.part2(input)
        self.assertEqual(result, '2713310158')

