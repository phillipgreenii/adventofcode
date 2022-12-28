def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

from typing import NamedTuple, List, Union, Tuple

Grid = List[List[str]]
Instructions = List[Union[int,str]]

def parse_instructions(line:str)->Instructions:
    instructions = []
    tmp_num = []
    for s in line:
        if ord('0') <= ord(s) <= ord('9'):
            tmp_num.append(s)
        else:
            if len(tmp_num) > 0:
                instructions.append(int("".join(tmp_num)))
                tmp_num = []
            instructions.append(s)
    if len(tmp_num) > 0:
        instructions.append(int("".join(tmp_num)))

    return instructions



def read_map_and_steps(file_name:str)->Tuple[Grid,Instructions]:
    lines = read_lines(file_name,skip_blanks=False)
    grid = []
    for line in lines:
        if line == '':
            break
        grid.append(list(line))
    instructions = parse_instructions(next(lines))
    return (grid,instructions)

def print_grid(grid:Grid):
    for row in grid:
        print("".join(row))

def part1(file_name):
    grid,instructions = read_map_and_steps(file_name)
    print_grid(grid)
    print(instructions)


print("part 1")
# 6032
print(part1('example.txt'))
# ?
# print(part1('input.txt'))

# print("part 2")
# # ?
# print(part2('example.txt'))
# # ?
# print(part2('input.txt'))