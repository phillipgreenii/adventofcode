import unittest

import support

import day10

class Tests(unittest.TestCase):

    def test_generate_signal(self):
        input = support.load_example("day10","example-small")
        result = day10.generate_signal(input)
        self.assertEqual(list(result), 
                         [(1, ''), (1, 'noop'), (1, 'addx'), (4, 'addx'), (4, 'addx'), (-1, 'addx')])

    def test_part1(self):
        input = support.load_example("day10","example")
        result = day10.part1(input)
        self.assertEqual(result, '13140')

    def test_part2(self):
        input = support.load_example("day10","example")
        result = day10.part2(input)
        expected = support.load_file("day10", "part2-example-answer").slurp()
        self.assertEqual(result, expected)


