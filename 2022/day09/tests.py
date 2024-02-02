import unittest

import support

import day09

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day09","example-small")
        result = day09.part1(input)
        self.assertEqual(result, '13')

    def test_part2_small(self):
        input = support.load_example("day09","example-small")
        result = day09.part2(input)
        self.assertEqual(result, '1')

    def test_part2_large(self):
        input = support.load_example("day09","example-large")
        result = day09.part2(input)
        self.assertEqual(result, '36')
