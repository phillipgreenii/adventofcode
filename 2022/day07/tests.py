import unittest

import support

import day07

class Tests(unittest.TestCase):

    def test_part1(self):
        input = support.load_example("day07","example")
        result = day07.part1(input)
        self.assertEqual(result, '95437')

    def test_part2(self):
        input = support.load_example("day07","example")
        result = day07.part2(input)
        self.assertEqual(result, '24933642')

