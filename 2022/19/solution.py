def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

from enum import Enum
from typing import NamedTuple, List, Iterator, Set, Dict

class Resource(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4

class Cost(NamedTuple):
    unit:int
    resource:Resource

# class RobotRecipe(NamedTuple):
#     type:Resource
#     cost:Cost

class BluePrint(NamedTuple):
    id:int
    recipes:Dict[Resource,List[Cost]]

def print_blue_print(blue_print):
    print(f"Blue Print {blue_print.id}")
    for r,cs in blue_print.recipes.items():
        cost = ", ".join([f"{c.unit} {c.resource.name}" for c in cs])
        print(f"\t{r.name} Robot: {cost}")

def read_blue_prints(file_name: str) -> Iterator[BluePrint]:
    for line in read_lines(file_name):
        parts = line.split(':')
        id = int(parts[0][10:])
        parts = parts[1].split('.')
        recipes:Dict[Resource,List[Cost]] = dict()
        for recipe in parts:
            if recipe == '':
                continue
            r_parts = recipe.split("robot")
            type_str = r_parts[0].split(' ')[3].upper()
            type = Resource[type_str]
            c_parts = r_parts[1][7:].split('and')
            costs = []
            for c_part in c_parts:
                cp = c_part.strip().split(' ')
                u = int(cp[0])
                r_s = cp[1].upper()
                r = Resource[r_s]
                costs.append(Cost( u,r))
            recipes[type] = costs
        yield BluePrint(id,recipes)



        # parts = line.split(',')
        # yield LavaDroplet(int(parts[0]),int(parts[1]), int(parts[2]))


def part1(file_name):
    for blue_print in read_blue_prints(file_name):
        print_blue_print(blue_print)
    

    
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
# 64
print(part1('example.txt'))
# 3068
# print(part1('input.txt'))

# print("part 2")
# # 93
# print(part2('example.txt'))
# # 23958
# print(part2('input.txt'))