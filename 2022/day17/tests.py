import unittest

import support

import day17

class Tests(unittest.TestCase):

    def test_part1_11(self):
        input = support.load_example("day17","example")
        result = day17.part1(input,11)
        self.assertEqual(result, '18')

    def test_part1_2022(self):
        input = support.load_example("day17","example")
        result = day17.part1(input,2022)
        self.assertEqual(result, '3068')

    def test_part2(self):
        input = support.load_example("day17","example")
        result = day17.part2(input, 1_000_000_000_000)
        self.assertEqual(result, '1514285714288')


# print("part 1")
# # 18
# print(part1('example.txt',11))
# # 3068
# print(part1('example.txt',2022))
# # 3239
# print(part1('input.txt',2022))

# print("part 2")
# # 1514285714288
