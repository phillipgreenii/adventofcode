def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

import json
def parse_line(line):
    return json.loads(line)

def read_packets(file_name):
    for line in read_lines(file_name):
        yield parse_line(line)

def read_packet_pairs(file_name):
    packets = read_packets(file_name)

    while True:
        try:
            left = next(packets)
            right = next(packets)
            yield (left, right)
        except StopIteration:
            break    

def clamp(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def compare_ints(left, right):
    return clamp(left - right)

def compare_lists(left, right):
    for ll,rr in zip(left,right):
        r = compare_anys(ll,rr)
        if r != 0:
            return r
    return clamp(len(left) - len(right))

def compare_anys(left, right):
    if isinstance(left, int) and isinstance(right,int):
        return compare_ints(left,right)
    if isinstance(left, int):
        left = [left]
    if isinstance(right,int):
        right = [right]
    return compare_lists(left,right)

def is_in_correct_order(left,right):
    return compare_anys(left,right) <= 0

def part1(file_name):

    in_correct_order = set()
    for index, (left, right) in enumerate(read_packet_pairs(file_name), start=1):
        if is_in_correct_order(left,right):
            in_correct_order.add(index)
    # print(in_correct_order)
    return sum(in_correct_order)

import math
from functools import cmp_to_key

def part2(file_name):
    divider_packets = [ [[2]], [[6]] ]
    packets = list(read_packets(file_name)) + divider_packets
    packets = sorted(packets, key=cmp_to_key(compare_anys))
    # for p in packets:
    #     print(p)
    key_parts = []
    for dp in divider_packets:
        key_parts.append(packets.index(dp)+1)
    print(key_parts)
    return math.prod(key_parts)

print("part 1")
# 13
print(part1('example.txt'))
# 5588
print(part1('input.txt'))

print("part 2")
# 140
print(part2('example.txt'))
# 23958
print(part2('input.txt'))