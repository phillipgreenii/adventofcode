import unittest

import support

import day18

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day18","example")
        result = day18.part1(input)
        self.assertEqual(result, '64')

    def test_part2(self):
        input = support.load_example("day18","example")
        result = day18.part2(input)
        self.assertEqual(result, '58')
