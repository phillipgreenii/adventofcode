from support import Input

from typing import NamedTuple, List, Iterator, Set, Dict, Optional, Tuple, Union
from functools import lru_cache
from heapq import heappush,heappop,heapify

class Point(NamedTuple):
    row:int
    col:int

class Blizzard(NamedTuple):
    point:Point
    direction:str

    def move_to(self, new_point:Point)->"Blizzard":
        return Blizzard(new_point,self.direction)

class Grid(NamedTuple):
    height:int
    width:int
    start:Point
    end:Point

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
    minutes:int
    expedition:Point
    distance_to_goal:int

    def score(self)->int:
        return self.minutes+self.distance_to_goal

    def __lt__(self,other:'State'):
        return self.score() < other.score()

class Searcher:

    def __init__(self, grid:Grid, blizzards:Tuple[Blizzard,...]):
        self.grid = grid
        self.blizzards_per_minute = {0:(blizzards,self._extract_points(blizzards))}

    def _extract_points(self,blizzards:Tuple[Blizzard,...])->Set[Point]:
        return set([b.point for b in blizzards])

    def _move_point(self,point:Point,direction:str)->Point:
        if direction == 'v':
            return Point(point.row+1,point.col)
        elif direction == '^':
            return Point(point.row-1,point.col)
        elif direction == '>':
            return Point(point.row,point.col+1)
        elif direction == '<':
            return Point(point.row,point.col-1)   

    def _move_blizzard(self,blizzard:Blizzard)->Blizzard:
        # move
        point = self._move_point(blizzard.point, blizzard.direction)
        # wrap if necessary
        if point.row == 0:
            point =  Point(self.grid.height-1-1,point.col)
        if point.row == self.grid.height-1:
            point =  Point(1,point.col)
        if point.col == 0:
            point =  Point(point.row,self.grid.width-1-1)
        if point.col == self.grid.width-1:
            point =  Point(point.row,1)
        return blizzard.move_to(point)

    def _move_blizzards(self, blizzards: Tuple[Blizzard,...])->Tuple[Blizzard,...]:
        return [ self._move_blizzard(b) for b in blizzards ]

    def _retrieve_blizzards_for(self,minute:int)->Tuple[Tuple[Blizzard,...],Set[Point]]:
        while len(self.blizzards_per_minute)<=minute:
            l = len(self.blizzards_per_minute)
            blizzards = self._move_blizzards(self.blizzards_per_minute[l-1][0])
            self.blizzards_per_minute[l] = (blizzards,self._extract_points(blizzards))
        # print(len(self.blizzards_per_minute))
        # print(minute)
        return self.blizzards_per_minute[minute]

    def _tick(self,state:State, expedition_movement:str=None)->State:
        # move expidition
        if expedition_movement is not None:
            expedition = self._move_point(state.expedition, expedition_movement)
        else:
            expedition = state.expedition
        return State(state.minutes+1, expedition, distance(self.grid.end, expedition))

    def _determine_next_moves(self,current_state:State)->Iterator[State]:
        # store future because we can look at future position of blizzards
        yield self._tick(current_state)
        blizzard_positions = self._retrieve_blizzards_for(current_state.minutes+1)[1]
        
        for direction in ['v','>','^','<']:
            p = self._move_point(current_state.expedition, direction)
            if p not in blizzard_positions and self.grid.is_valid_move(p):
                yield self._tick(current_state, direction)

    def search(self)->Tuple[State,State]:
        initial_state = State(0,self.grid.start,distance(self.grid.start,self.grid.end))

        best_solution_score = float('inf')
        queue = [initial_state]
        tried = set()
        goal_state = None
        # c = 0
        while queue:
            # c += 1
            # if c % 100 == 0:
            #     print(len(queue))
            #     print(move_blizzards.cache_info())
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
                goal_state = current_state
                best_solution_score = goal_state.score()
                queue = list(filter(lambda s: s.score()<=best_solution_score,queue))
                if len(queue) > 0:
                    heapify(queue)
            for new_state in self._determine_next_moves(current_state):
                if new_state not in tried and new_state.score() <= best_solution_score:
                    heappush(queue,new_state)
                    tried.add(new_state)

        return (initial_state, goal_state)

    def print_state(self, state:State)->None:
        blizzards = {}
        for b in self._retrieve_blizzards_for(state.minutes)[0]:
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
        for r in range(self.grid.height):
            line = []
            for c in range(self.grid.width):
                p = Point(r,c)
                if state.expedition == p:
                    line.append('E')
                elif self.grid.start == p :
                    line.append('.')
                elif self.grid.end == p:
                    line.append('.')
                elif p in blizzards:
                    line.append(blizzards[p])
                elif r == 0 or c == 0 or r == self.grid.height-1 or c == self.grid.width-1:
                    line.append("#")
                else:
                    line.append('.')
            print("".join(line))


def read_paramaters(input:Input)->Tuple[Grid,Tuple[Blizzard,...]]:
    height = 0
    width = 0
    blizzards=[]
    for line in input.lines(skip_blanks=True):
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

    return (grid,tuple(blizzards))

def part1(input:Input)->str:
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

    grid,blizzards = read_paramaters(input)
    # print(grid)
    # print(blizzards)
    searcher = Searcher(grid,blizzards)
    initial_state, final_state = searcher.search()
    searcher.print_state(initial_state)
    searcher.print_state(final_state)

    # print(state)
    # print_state(state)
    # state = search(state)
    # print(state)
    # state = tick(state,'v')
    # print_state(state)
    # plus 1 because this code is 0 based but problem expects 1 based
    return str(final_state.minutes + 1)
