import unittest

import support

import day22

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day22","example")
        result = day22.part1(input)
        self.assertEqual(result, '6032')

    def test_part2(self):
        input = support.load_example("day22","example")
        result = day22.part2(input)
        self.assertEqual(result, '5031')

