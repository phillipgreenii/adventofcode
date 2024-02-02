import unittest

import support

import day05

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day05","example")
        result = day05.part1(input)
        self.assertEqual(result, 'CMZ')

    def test_part2(self):
        input = support.load_example("day05","example")
        result = day05.part2(input)
        self.assertEqual(result, 'MCD')
