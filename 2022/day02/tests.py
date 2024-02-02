import unittest

import support

import day02

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day02","example")
        result = day02.part1(input)
        self.assertEqual(result, '15')

    def test_part2(self):
        input = support.load_example("day02","example")
        result = day02.part2(input)
        self.assertEqual(result, '12')

