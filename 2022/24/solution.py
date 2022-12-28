def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

from enum import Enum
from typing import NamedTuple, List, Iterator, Set, Dict, Optional, Tuple, Union

class Point(NamedTuple):
    row:int
    col:int

class Blizzard(NamedTuple):
    point:Point
    direction:str

    # def __init__(self,point:Point,direction:str):
    #     self.point = point
    #     self.direction = direction

    def move_to(self, new_point:Point)->"Blizzard":
        return Blizzard(new_point,self.direction)


class Grid(NamedTuple):
    # blizzards:List[Blizzard]
    height:int
    width:int
    start:Point
    end:Point
    # expedition:Point

    def is_wall(self, point:Point)->bool:
        if point == self.start or point == self.end:
            return False
        return point.row == 0 or point.col == 0 or point.row == self.height-1 or point.col == self.width-1

    def is_valid_move(self, point:Point)->bool:
        if point == self.start or point == self.end:
            return True
        return 1 <= point.row <= self.height-1-1 and 1 <= point.col <= self.width-1-1 

def distance(p1:Point,p2:Point)->int:
    return abs(p1.row-p2.row) + abs(p1.col-p2.col)

class State(NamedTuple):
    grid:Grid
    minutes:int
    blizzards:Tuple[Blizzard,...]
    expedition:Point
    distance_to_goal:int

    def update(self, blizzards:Tuple[Blizzard,...], expedition:Point)->"State":
        return State(self.grid, self.minutes+1,blizzards, expedition, distance(self.grid.end, expedition))

    def __lt__(self,other:'State'):
        if self.minutes != other.minutes:
            return self.minutes < other.minutes
        if self.distance_to_goal != other.distance_to_goal:
            return self.distance_to_goal < other.distance_to_goal
        return False

    def debug(self)->str:
        return f"S[{self.minutes}:{self.distance_to_goal}:{self.expedition}]"

def read_initial_state(file_name:str)->State:
    height = 0
    width = 0
    blizzards=[]
    for line in read_lines(file_name):
        width = len(line)
        for c,s in enumerate(line):
            p = Point(height, c)
            if s == '.':
                if height == 0:
                    start = p
                else:
                    end = p
            if s == '<' or s == '>' or s == '^' or s == 'v':
                blizzards.append(Blizzard(p,s))
        height += 1
    grid = Grid(height,width,start,end)

    return State(grid,0,tuple(blizzards),start, distance(start,end))

def print_state(state:State)->None:
    blizzards = {}
    for b in state.blizzards:
        v = blizzards.get(b.point, None)
        if v is None:
            v = b.direction
        elif v == '3':
            v = '4'
        elif v == '2':
            v = '3'
        else:
            v = '2'
        blizzards[b.point] = v
    print(f"Minute: {state.minutes}")
    for r in range(state.grid.height):
        line = []
        for c in range(state.grid.width):
            p = Point(r,c)
            if state.expedition == p:
                line.append('E')
            elif state.grid.start == p :
                line.append('.')
            elif state.grid.end == p:
                line.append('.')
            elif p in blizzards:
                line.append(blizzards[p])
            elif r == 0 or c == 0 or r == state.grid.height-1 or c == state.grid.width-1:
                line.append("#")
            else:
                line.append('.')
        print("".join(line))


def move_point(point:Point,direction:str)->Point:
    if direction == 'v':
        return Point(point.row+1,point.col)
    elif direction == '^':
        return Point(point.row-1,point.col)
    elif direction == '>':
        return Point(point.row,point.col+1)
    elif direction == '<':
        return Point(point.row,point.col-1)   

def move_blizzard(grid:Grid,blizzard:Blizzard)->Blizzard:
    # move
    point = move_point(blizzard.point, blizzard.direction)
    # if blizzard.direction == 'v':
    #     point =  Point(blizzard.point.row+1,blizzard.point.col)
    # elif blizzard.direction == '^':
    #     point =  Point(blizzard.point.row-1,blizzard.point.col)
    # elif blizzard.direction == '>':
    #     point =  Point(blizzard.point.row,blizzard.point.col+1)
    # elif blizzard.direction == '<':
    #     point =  Point(blizzard.point.row,blizzard.point.col-1)
    # wrap if necessary
    if point.row == 0:
        point =  Point(grid.height-1-1,point.col)
    if point.row == grid.height-1:
        point =  Point(1,point.col)
    if point.col == 0:
        point =  Point(point.row,grid.width-1-1)
    if point.col == grid.width-1:
        point =  Point(point.row,1)
    return blizzard.move_to(point)

def move_expedition(grid:Grid, current_point:Point, direction:str)->Point:
    return move_point(current_point, direction)

def tick(state:State, expedition_movement:str=None)->State:
    # move blizzards
    blizzards = [ move_blizzard(state.grid, b) for b in state.blizzards ]
    # move expidition
    if expedition_movement is not None:
        expedition = move_expedition(state.grid,state.expedition, expedition_movement)
    else:
        expedition = state.expedition
    return state.update(tuple(blizzards),expedition)
   

def simulate(file_name, iterations):
    state = read_initial_state(file_name)
    print_state(state)
    for _ in range(iterations):
        state = tick(state)
        print_state(state)

def determine_next_moves(current_state:State)->Iterator[State]:
    # store future because we can look at future position of blizzards
    future = tick(current_state)
    blizzard_positions = set([b.point for b in future.blizzards])
    # wait
    yield future
    for direction in ['v','>','^','<']:
        p = move_point(current_state.expedition, direction)
        if p not in blizzard_positions and current_state.grid.is_valid_move(p):
            yield tick(current_state, direction)

        


from heapq import heappush,heappop
def search(initial_state:State):
    queue = [initial_state]
    tried = set()
    # track duplicates?
    while queue:
        # print(", ".join([s.debug() for s in queue]))
        # if len(queue) > 1000:
        #     raise Exception("queue too large")
        # print(len(queue))
        current_state = heappop(queue)
        # if current_state.minutes>20:
        #     raise Exception("too many minutes")
        tried.add(current_state)
        # print(current_state.debug())
        if current_state.distance_to_goal == 0:
            return current_state
        for new_state in determine_next_moves(current_state):
            if new_state not in tried:
                heappush(queue,new_state)
                tried.add(new_state)


def part1(file_name)->str:
    # s1 = State(None,1,(),None,1)
    # s2 = State(None,1,(),None,2)
    # s3 = State(None,2,(),None,1)
    # s4 = State(None,2,(),None,2)

    # h= []
    # for s in [s4,s2,s3,s1]:
    #     heappush(h,s)
    # # print(h)
    # l = [heappop(h).debug() for i in range(len(h))]
    # print(l)

    state = read_initial_state(file_name)
    # print(state)
    print_state(state)
    state = search(state)
    # print(state)
    # state = tick(state,'v')
    print_state(state)
    # plus 1 because this code is 0 based but problem expects 1 based
    return state.minutes + 1
   


print("part 1")
# simulate('simple-example.txt',5)
# simulate('example.txt',5)
# 11
print(part1('simple-example.txt'))
# 18
print(part1('example.txt'))
# ?
# print(part1('input.txt'))

# print("part 2")
# ?
# print(part2('example.txt'))
# ?
# print(part2('input.txt'))