from support import Input, load_file

from typing import NamedTuple, List
from collections import namedtuple
# Valve = namedtuple('Valve', 'id rate leads')
class Valve(NamedTuple):
    id: str
    rate: int
    leads: List[str]

# Position = namedtuple('Position', 'r c')
class Position(NamedTuple):
    r:int
    c:int

class Shape:
    def __init__(self, grid):
        self._grid = grid
    
    def at(self, pos:Position)->str:
        return self._grid[pos.r][pos.c]

    @property
    def height(self)->int:
        return len(self._grid)
    
    @property
    def width(self)->int:
        return len(self._grid[0])

    def __repr__(self):
        return f"{self._grid}"



class Chamber:

    def __init__(self,rock_shapes:List[Shape], jet_pattern:List[str], width:int=7, starting_left_gap:int=2,starting_bottom_gap:int=3):
        self.rock_shape_generator = itertools.cycle(rock_shapes)
        self.jet_generator = itertools.cycle(jet_pattern)
        self.width = width
        self.height = 0
        self.starting_left_gap = starting_left_gap
        self.starting_bottom_gap = starting_bottom_gap
        self.grid = []
        self.lines_removed = 0

    def _next_shape(self) -> Shape:
        return next(self.rock_shape_generator)

    def _next_jet(self) -> str:
        return next(self.jet_generator)

    def _expand(self,shape:Shape,position:Position) -> None:
        while (position.r+shape.height) >= len(self.grid):
            self.grid.append([cell_nothing]*self.width)

    def _next_rock(self)->"Rock":
        shape = self._next_shape()
        position = Position(self.height+self.starting_bottom_gap,self.starting_left_gap)
        self._expand(shape,position)

        return Rock(self,shape,position)

    def _is_valid(self,rock:'Rock') -> bool:
        for i in range(rock.shape.height):
            r = rock.position.r + i
            for j in range(rock.shape.width): 
                c = rock.position.c + j
                # print(f"{i},{j}:{shape}")
                if rock.shape.at(Position(i,j)) != cell_nothing\
                    and self.grid[r][c] != cell_nothing:
                    return False
        return True

    def total_height(self):
        return self.height + self.lines_removed

    def __apply_rock_to_grid(self, grid:List[List[str]],rock:'Rock', symbol_override:str=None):
        for i in range(rock.shape.height):
            r = rock.position.r + i
            for j in range(rock.shape.width): 
                c = rock.position.c + j
                v = rock.shape.at(Position(i,j))
                # print(f"{i},{j}:{shape}")
                if v == cell_rock:
                    # print(f"{y},{x}:{self.grid}")
                    grid[r][c] = symbol_override if symbol_override else v
        # for r in range(len(self.grid)-1,-1,-1):
        #     if cell_rock in self.grid[r]:
        #         self.height = r + 1
        #         break


    def _apply_rock(self,rock:'Rock') -> None:
        self.__apply_rock_to_grid(self.grid, rock)
        # update height
        for r in range(len(self.grid)-1,-1,-1):
            # print(f"rock ({cell_rock}) in {self.grid[r]}? {cell_rock in self.grid[r]}")
            if cell_rock in self.grid[r]:
                self.height = r + 1
                break

    def _remove_coverred_lines(self) -> None:
        lowest_relevant_height = self.height
        for c in range(self.width):
            for r in range(self.height-1,0-1,-1):
                if self.grid[r][c] == '#':
                    lowest_relevant_height = min(lowest_relevant_height,r)
                    break
        if lowest_relevant_height > 0:
            # print(f"removing {lowest_relevant_height}")
            self.grid = self.grid[lowest_relevant_height:]
            self.lines_removed += lowest_relevant_height
            self.height -= lowest_relevant_height

    def drop_rock(self) -> None:
        # print(f"height:{self.height}")
        rock = self._next_rock()
        done = False
        def make_move(direction)->bool:
            # print(f"trying {direction}")
            can_move = rock.move(direction)
            if not can_move:
                # print("no move")
                return False
            if not self._is_valid(rock):
                # print("invalid move")
                rock.undo(direction)
                return False
            # print("moved")
            return True
        # NOTE: this prints the next shape at its initial position
        # print(self._dump_to_str(rock))
        while not done:
            # move left-right
            direction = self._next_jet()
            make_move(direction)
            # move down
            if not make_move('v'):
                done = True
        self._apply_rock(rock)
        self._remove_coverred_lines()

    def _dump_to_str(self,moving_rock=None):
        if moving_rock:
            import copy
            g = copy.deepcopy(self.grid)
            self.__apply_rock_to_grid(g,moving_rock,cell_shape)
        else:
            g = self.grid

        lines = []
        # for r in range(self.height):
        for r in range(len(g)-1,-1,-1):
            lines.append('|' + ''.join(g[r]) + '|')
        if self.lines_removed == 0:
            lines.append('+' + ('-'*self.width) + '+')
        else:
            lines.append('|' + '⋮'.center(self.width) + '|')
            lines.append('|' + str(self.lines_removed).center(self.width) + '|')
        
        return '\n'.join(lines)

    def __repr__(self) -> str:
        return self._dump_to_str()

class Rock:
    def __init__(self,chamber:Chamber,shape:Shape,position:Position):
        self._chamber = chamber
        self.shape = shape
        self.position = position

    def move(self,direction) -> bool:
        if direction == '<':
            if self.position.c == 0:
                return False
            else:
                self.position = Position(self.position.r,self.position.c-1)
                return True
        elif direction == '>':
            if self.position.c + self.shape.width == self._chamber.width:
                return False
            else:
                self.position = Position(self.position.r,self.position.c+1)
                return True
        elif direction == 'v':
            if self.position.r == 0:
                return False
            else:
                self.position = Position(self.position.r-1, self.position.c)
                return True
        else:
            raise Exception(f"Unsupported direction:{direction}")

    def undo(self,direction) -> None:
        if direction == '<':
            self.position = Position(self.position.r,self.position.c+1)
        elif direction == '>':
            self.position = Position(self.position.r,self.position.c-1)
        elif direction == 'v':
            self.position = Position(self.position.r+1, self.position.c)
        else:
            raise Exception(f"Unsupported direction:{direction}")


def read_shapes(input:Input) -> List[Shape]:
    shapes = []
    shape = []
    for line in input.lines():
        if line == '':
            shapes.append(shape[::-1])
            shape = []
        else:
            shape.append(list(line)) 
    if len(shape) > 0:
        shapes.append(shape[::-1])
    return list(map(lambda g: Shape(g),shapes))

def read_jet_pattern(input:Input) -> List[str]:
    return list(input.slurp())

import itertools

cell_nothing = '.'
cell_rock = '#'
cell_shape = '@'

def simulate_rock_drops(shapes_input:Input, input:Input, drops):
    shapes = read_shapes(shapes_input)
    # print(shapes)
    jet_pattern = read_jet_pattern(input)
    # print(jet_pattern)
    chamber = Chamber(shapes,jet_pattern)
    # print(chamber)
    for i in range(drops):
        # print(i)
        chamber.drop_rock()
        # print(f"{i+1}:{chamber.height}")
        # print(chamber)
    # print(str(chamber))
    return chamber.total_height()

# load_file
def part1(input:Input, drops=2022)->str:
    return str(simulate_rock_drops(load_file("day17",'shapes'),input,drops))
 
def part2(input:Input, drops=1_000_000_000_000):
    # return str(simulate_rock_drops(load_file("day17",'shapes'),input,drops))
    # disabling this test because tests would take too long
    return "disabled"
