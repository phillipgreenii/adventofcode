import unittest

import support

import day24

class Tests(unittest.TestCase):

    def test_part1_simple(self):
        input = support.load_example("day24","example-simple")
        result = day24.part1(input)
        # NOTE: should be 10 or 11?
        self.assertEqual(result, '11')

    def test_part1_complex(self):
        input = support.load_example("day24","example-complex")
        result = day24.part1(input)
        self.assertEqual(result, '18')

    def test_part2(self):
        input = support.load_example("day24","example-complex")
        result = day24.part2(input)
        self.assertEqual(result, 'NOT_IMPLEMENTED')

