import unittest

import support

import day08

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day08","example")
        result = day08.part1(input)
        self.assertEqual(result, '21')

    def test_part2(self):
        input = support.load_example("day08","example")
        result = day08.part2(input)
        self.assertEqual(result, '8')

