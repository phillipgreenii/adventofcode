import unittest

import support

import day20

class Tests(unittest.TestCase):


    def test_rotate(self):
        tests = [
            ([ 1,  2, -3,  3, -2,  0,  4], 1,[ 2,  1, -3,  3, -2,  0,  4]),
            ([ 2,  1, -3,  3, -2,  0,  4], 2,[ 1, -3,  2,  3, -2,  0,  4]),
            ([ 1, -3,  2,  3, -2,  0,  4],-3,[ 1,  2,  3, -2, -3,  0,  4]),
            ([ 1,  2,  3, -2, -3,  0,  4], 3,[ 1,  2, -2, -3,  0,  3,  4]),
            ([ 1,  2, -2, -3,  0,  3,  4],-2,[ 1,  2, -3,  0,  3,  4, -2]),
            ([ 1,  2, -3,  0,  3,  4, -2], 0,[ 1,  2, -3,  0,  3,  4, -2]),
            ([ 1,  2, -3,  0,  3,  4, -2], 4,[ 1,  2, -3,  4,  0,  3, -2]),
        ]

        for l,x,expected_result in tests:
            with self.subTest(l=l,x=x,expected_result=expected_result):
                day20.rotate(l,x)
                self.assertEqual(l, expected_result)
            
    def test_wrap_position(self):
        max_len = 7
        tests = [
            (-6  ,6),
            (0   ,6),
            (6   ,6),
            (-1  ,5),
            (5   ,5),
            (1   ,1),
            (3+ 1,4),
            (1+-2,5)
        ]

        for p,ev in tests:
            with self.subTest(p=p,ev=ev):
                v = day20.wrap_position(max_len,p)
                self.assertEqual(v, ev)

    def test_part1(self):
        input = support.load_example("day20","example")
        result = day20.part1(input)
        self.assertEqual(result, '3')

    def test_part2(self):
        input = support.load_example("day20","example")
        result = day20.part2(input)
        self.assertEqual(result, 'NOT_IMPLEMENTED')

