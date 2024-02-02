import unittest

import support

import day16

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day16","example")
        result = day16.part1(input)
        self.assertEqual(result, '1651')

    def test_part2(self):
        input = support.load_example("day16","example")
        result = day16.part2(input)
        self.assertEqual(result, '1707')

