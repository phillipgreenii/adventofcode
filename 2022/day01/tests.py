import unittest

import support

import day01

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day01","example")
        result = day01.part1(input)
        self.assertEqual(result, '24000')

    def test_part2(self):
        input = support.load_example("day01","example")
        result = day01.part2(input)
        self.assertEqual(result, '45000')
   