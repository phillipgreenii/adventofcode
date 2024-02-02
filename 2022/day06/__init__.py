from support import Input

from collections import deque

def find_first_unique_set_of_size(size, signal):
    for i in range(size-1, len(signal)):
        window = signal[(i-size):i]
        # print(window)
        uniq_symbols = set(window)
        # print(uniq_symbols)
        if len(uniq_symbols) == size:
            return i
    return None

def part1(input:Input)->str:
    return str(find_first_unique_set_of_size(4, input.slurp()))

def part2(input:Input)->str:
    return str(find_first_unique_set_of_size(14, input.slurp()))
