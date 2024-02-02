import unittest

import support

import day03

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day03","example")
        result = day03.part1(input)
        self.assertEqual(result, '157')

    def test_part2(self):
        input = support.load_example("day03","example")
        result = day03.part2(input)
        self.assertEqual(result, '70')

