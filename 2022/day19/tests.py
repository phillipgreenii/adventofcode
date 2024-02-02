import unittest

import support

import day19

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day19","example")
        result = day19.part1(input)
        self.assertEqual(result, '33')

    def test_part2(self):
        input = support.load_example("day19","example")
        result = day19.part2(input)
        self.assertEqual(result, 'NOT_IMPLEMENTED')

