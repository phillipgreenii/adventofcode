from support import Input

from typing import NamedTuple, List, Set
from collections import defaultdict

class Point(NamedTuple):
    row:int
    col:int

    def add(self, point:"Point")->"Point":
        # print(f"adding {point}")
        return Point(self.row+point.row,self.col+point.col)

def read_elves(input:Input)->List[Point]:
    elves = []
    for r,line in enumerate(input.lines(skip_blanks=True)):
        for c,s in enumerate(line):
            if s == '#':
                elves.append(Point(r,c))
    return elves

def determine_min_max(elves:List[Point]):
    r_min = float('inf')
    r_max = float('-inf')
    c_min = float('inf')
    c_max = float('-inf')
    for r,c in elves:
        r_min = min(r,r_min)
        r_max = max(r,r_max)
        c_min = min(c,c_min)
        c_max = max(c,c_max)
    return (r_min, r_max,c_min,c_max)


def print_elves(elves:List[Point]):
    r_min, r_max,c_min,c_max = determine_min_max(elves)
    for r in range(r_min,r_max+1):
        line = []
        for c in range(c_min,c_max+1):
            if Point(r,c) in elves:
                line.append('#')
            else:
                line.append('.')
        print("".join(line))

N  = Point(-1, 0)
NW = Point(-1,-1)
W  = Point( 0,-1)
SW = Point( 1,-1)
S  = Point( 1, 0)
SE = Point( 1, 1)
E  = Point( 0, 1)
NE = Point(-1, 1)

direction_checks = [
    # north
    (N,(N,NW,NE)),
    # south
    (S,(S,SW,SE)),
    # west
    (W,(W,NW,SW)),
    # east
    (E,(E,NE,SE)),
]

def determine_round_moves(round:int):
    yield direction_checks[(round+0)%4]
    yield direction_checks[(round+1)%4]
    yield direction_checks[(round+2)%4]
    yield direction_checks[(round+3)%4]

def find_next_move(current_locations:Set[Point],moves,elf:Point)->Point:
    nearby = False
    for m in [N,S,E,W,NE,NW,SE,SW]:
        if elf.add(m) in current_locations:
            nearby = True
            break
    if not nearby:
        return elf

    for movement,moves_to_check in moves:
        available = True
        for s in moves_to_check:
            # print(s)
            p = elf.add(s)
            if p in current_locations:
                available = False
                break
        if available:
            return elf.add(movement)
    return elf

def walk_elves(elves:List[Point], round:int):
    moves = list(determine_round_moves(round))
    # for m in moves:
    #     print(m)
    current_locations = set(elves)
    potential_moves = []
    new_locations = defaultdict(lambda:0)

    for elf in elves:
       m = find_next_move(current_locations, moves, elf)
       potential_moves.append(m)
       new_locations[m] += 1
    # print(new_locations)
    # for k,v in new_locations.items():
    #     print(f"{k}:{v}")

    for i in range(len(elves)):
        if new_locations[potential_moves[i]] > 1:
            # if mulitple elves are moving to new spot, don't move
            potential_moves[i] = elves[i]

    return potential_moves

def count_empty_tiles(elves:List[Point]):
    r_min, r_max,c_min,c_max = determine_min_max(elves)
    total_area = (r_max-r_min+1)*(c_max-c_min+1)
    return total_area - len(elves)

def part1(input:Input)->str:
    elves = read_elves(input)
    # print(elves)
    # print_elves(elves)

    for i in range(10):
        elves = walk_elves(elves,i)
        # print(i)
        # print_elves(elves)
    # print_elves(elves)
    return str(count_empty_tiles(elves))
     
def part2(input:Input)->str:
    elves = read_elves(input)
    # print(elves)
    # print_elves(elves)

    counter = 0
    while True:
        p_elves = elves
        elves = walk_elves(elves,counter)
        counter+=1
        if elves == p_elves:
            break
        # print(i)
        # print_elves(elves)
    # print_elves(elves)
    return str(counter)
