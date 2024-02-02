import unittest

import support

import day21

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day21","example")
        result = day21.part1(input)
        self.assertEqual(result, '152')

    def test_part2(self):
        input = support.load_example("day21","example")
        result = day21.part2(input)
        self.assertEqual(result, '301')
