import unittest

import support

import day25

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day25","example")
        result = day25.part1(input)
        self.assertEqual(result, '2=-1=0')

    def test_part2(self):
        input = support.load_example("day25","example")
        result = day25.part2(input)
        self.assertEqual(result, 'NOT_IMPLEMENTED')

