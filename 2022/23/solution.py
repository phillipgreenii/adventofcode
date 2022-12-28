def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

from typing import NamedTuple, List

class Point(NamedTuple):
    row:int
    col:int

def read_elves(file_name:str)->List[Point]:
    elves = []
    for r,line in enumerate(read_lines(file_name)):
        for c,s in enumerate(line):
            if s == '#':
                elves.append(Point(r,c))
    return elves

def print_elves(elves:List[Point]):
    r_min = float('inf')
    r_max = float('-inf')
    c_min = float('inf')
    c_max = float('-inf')
    for r,c in elves:
        r_min = min(r,r_min)
        r_max = max(r,r_max)
        c_min = min(c,c_min)
        c_max = max(c,c_max)
    for r in range(r_min,r_max+1):
        line = []
        for c in range(c_min,c_max+1):
            if Point(r,c) in elves:
                line.append('#')
            else:
                line.append('.')
        print("".join(line))



def part1(file_name):
    elves = read_elves(file_name)
    # print(elves)
    print_elves(elves)
     
# def part2(file_name):
#     paths = list(read_rock_paths(file_name))
#     cave = build_cave(paths, True)
#     grains_dropped = 0
#     while cave.drop_sand():
#         grains_dropped += 1
#     # for _ in range(94):
#     #     cave.drop_sand()
#     # print(cave)

#     return grains_dropped

print("part 1")
# 110
print(part1('example.txt'))
# ?
# print(part1('input.txt'))

# print("part 2")
# # ?
# print(part2('example.txt'))
# # ?
# print(part2('input.txt'))