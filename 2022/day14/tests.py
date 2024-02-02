import unittest

import support

import day14

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day14","example")
        result = day14.part1(input)
        self.assertEqual(result, '24')

    def test_part2(self):
        input = support.load_example("day14","example")
        result = day14.part2(input)
        self.assertEqual(result, '93')

