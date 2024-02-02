from support import Input

from typing import NamedTuple, List, Union, Tuple, Dict,Iterator,Optional

class Point(NamedTuple):
    row:int
    col:int

class Tile:
    point:Point
    symbol:str
    right:"Tile"  
    down:"Tile"
    left:"Tile"
    up:"Tile"  
    def __init__(self,point:Point,symbol:str):
        self.point = point
        self.symbol = symbol
        self.right = None
        self.down = None
        self.left = None
        self.up = None

    def __repr__(self):
        r = self.right.symbol if self.right else None
        d = self.down.symbol if self.down else None
        l = self.left.symbol if self.left else None
        u = self.up.symbol if self.up else None
        return f"Tile({(self.point,self.symbol,r,d,l,u)})"

class Grid:
    width:int
    height:int
    tiles:Dict[Point,Tile]

    def __init__(self, width:int, height:int, tiles:Dict[Point,Tile]):
        self.width = width
        self.height = height
        self.tiles = tiles

    def lookup(self,point:Point)->Optional[Tile]:
        # TODO add range check
        return self.tiles.get(point, None)

    def at(self, point:Point)->str:
        # TODO add range check
        if point in self.tiles:
            return self.tiles[point].symbol
        else:
            return ' '

Instructions = List[Union[int,str]]

def parse_instructions(line:Iterator[str])->Instructions:
    instructions = []
    tmp_num = []
    for s in next(line):
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

def parse_grid(lines:Iterator[str])->Grid:
    tiles = {}
    width = float('-inf')
    height = 0
    # find all tiles
    for r,line in enumerate(lines):
        if line == '':
            break
        height = r + 1
        width = max(width,len(line))
        for c,s in enumerate(line):
            if s == '#' or s == '.':
                p = Point(r,c)
                t = Tile(p,s)
                tiles[p] = t
    
    # create grid
    grid = Grid(width, height, tiles)
        
    # for tile in grid.tiles.values():
    #     print(tile)

    return grid

def wrap_torus(grid:Grid)->Grid:
    
    # link tiles
    for tile in grid.tiles.values():
        if tile.symbol != '.':
            continue
        if tile.up is None:
            t = grid.lookup(Point(tile.point.row-1,tile.point.col))
            if t and t.symbol == '.':
                tile.up = t
                t.down = tile
            elif not t or t.symbol == ' ':
                # wrap up
                # move down until find end of column
                p_t = t
                t = tile
                while t and t.symbol != ' ':
                    p_t = t
                    t = grid.lookup(Point(t.point.row+1,t.point.col))
                if p_t and p_t.symbol == '.':
                    tile.up= p_t
                    p_t.down = tile
        if tile.down is None:
            t = grid.lookup(Point(tile.point.row+1,tile.point.col))
            if t and t.symbol == '.':
                tile.down = t
                t.up = tile
            elif not t or t.symbol == ' ':
                # wrap down
                # move up until find end of column
                p_t = t
                t = tile
                while t and t.symbol != ' ':
                    p_t = t
                    t = grid.lookup(Point(t.point.row-1,t.point.col))
                if p_t and p_t.symbol == '.':
                    tile.down= p_t
                    p_t.up = tile
        if tile.left is None:
            t = grid.lookup(Point(tile.point.row,tile.point.col-1))
            if t and t.symbol == '.':
                tile.left = t
                t.right = tile
            elif not t or t.symbol == ' ':
                # wrap left
                # move up until find end of column
                p_t = t
                t = tile
                while t and t.symbol != ' ':
                    p_t = t
                    t = grid.lookup(Point(t.point.row,t.point.col+1))
                if p_t and p_t.symbol == '.':
                    tile.left= p_t
                    p_t.right = tile
        if tile.right is None:
            t = grid.lookup(Point(tile.point.row,tile.point.col+1))
            if t and t.symbol == '.':
                tile.right = t
                t.left = tile
            elif not t or t.symbol == ' ':
                # wrap right
                # move up until find end of column
                p_t = t
                t = tile
                while t and t.symbol != ' ':
                    p_t = t
                    t = grid.lookup(Point(t.point.row,t.point.col-1))
                if p_t and p_t.symbol == '.':
                    tile.right= p_t
                    p_t.left = tile
    return grid

class Direction(NamedTuple):
    value:int
    symbol:str

FACE_RIGHT = Direction(0,'>')
FACE_DOWN  = Direction(1,'v')
FACE_LEFT  = Direction(2,'<')
FACE_UP    = Direction(3,'^')

class State(NamedTuple):
    tile:Tile
    direction:Direction

def read_initial_state(input:Input)->Tuple[Grid,Instructions,Point]:
    lines = input.lines()
    grid = parse_grid(lines)
    instructions = parse_instructions(lines)

    starting_tile = min(list(grid.tiles.values()), key=lambda t: t.point.row * 10000 + t.point.col)

    return (grid,instructions, State(starting_tile, FACE_RIGHT))

def print_grid(grid:Grid, path:List[State]=[]):
    path_lookup = {s.tile.point:s.direction.symbol for s in path}

    for r in range(grid.height):
        line = []
        for c in range(grid.width):
            p = Point(r,c)
            if p in path_lookup:
                line.append(path_lookup[p])
            else:
                line.append(grid.at(p))
        print("".join(line))

def move(grid:Grid,state:State)->State:
    t = None
    if state.direction == FACE_LEFT:
        if state.tile.left:
            t = state.tile.left
    elif state.direction == FACE_RIGHT:
        if state.tile.right:
            t = state.tile.right
    elif state.direction == FACE_UP:
        if state.tile.up:
            t = state.tile.up
    elif state.direction == FACE_DOWN:
        if state.tile.down:
            t = state.tile.down
    else:
        raise Exception(f"Unknown Direction:{state.direction}")

    if t:
        return State(t,state.direction)
    else:
        return None

def rotate(state:State, rotation_direction:int)->State:
    v = state.direction.value + rotation_direction
    if v < 0:
        v = 3
    elif v > 3:
        v = 0

    if v == 0:
        d = FACE_RIGHT
    elif v == 1:
        d = FACE_DOWN
    elif v == 2:
        d = FACE_LEFT
    elif v == 3:
        d = FACE_UP
    else:
        raise Exception(f"Unknown rotation ({rotation_direction}) direction value: {v}")

    return State(state.tile, d)

def walk(grid:Grid, instructions:Instructions, initial_state:State)->State:
    path = [initial_state]
    state = initial_state
    for instruction in instructions:
        if isinstance(instruction, int):
            for _ in range(instruction):
                s = move(grid,state)
                if s:
                    state = s
                    path.append(state)
                else:
                    break
        elif instruction == 'R':
            state = rotate(state, 1)
        elif instruction == 'L':
            state = rotate(state,-1)
        else:
            raise Exception(f"Unknown Instruction: {instruction}")

    return state, path

def score_state(state:State)->int:
    # add one because puzzle is 1 based but this code is 0 based
    return (1000*(state.tile.point.row+1))+(4*(state.tile.point.col+1))+(state.direction.value)

def part1(input:Input)->str:
    grid,instructions, initial_state = read_initial_state(input)
    grid = wrap_torus(grid)
    # print_grid(grid)
    # print(instructions)
    # print(initial_state)
    final_state,path = walk(grid, instructions, initial_state)
    # print_grid(grid, path)

    return str(score_state(final_state))

def wrap_cube(grid:Grid)->Grid:
    
    # FIXME implement
    return grid

"""
As you reach the force field, you think you hear some Elves in the distance. Perhaps they've already arrived?

You approach the strange input device, but it isn't quite what the monkeys drew in their notes. Instead, you are met with a large cube; each of its six faces is a square of 50x50 tiles.

To be fair, the monkeys' map does have six 50x50 regions on it. If you were to carefully fold the map, you should be able to shape it into a cube!

In the example above, the six (smaller, 4x4) faces of the cube are:

        1111
        1111
        1111
        1111
222233334444
222233334444
222233334444
222233334444
        55556666
        55556666
        55556666
        55556666
You still start in the same position and with the same facing as before, but the wrapping rules are different. Now, if you would walk off the board, you instead proceed around the cube. From the perspective of the map, this can look a little strange. In the above example, if you are at A and move to the right, you would arrive at B facing down; if you are at C and move down, you would arrive at D facing up:

        ...#
        .#..
        #...
        ....
...#.......#
........#..A
..#....#....
.D........#.
        ...#..B.
        .....#..
        .#......
        ..C...#.
Walls still block your path, even if they are on a different face of the cube. If you are at E facing up, your movement is blocked by the wall marked by the arrow:

        ...#
        .#..
     -->#...
        ....
...#..E....#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.
Using the same method of drawing the last facing you had with an arrow on each tile you visit, the full path taken by the above example now looks like this:

        >>v#    
        .#v.    
        #.v.    
        ..v.    
...#..^...v#    
.>>>>>^.#.>>    
.^#....#....    
.^........#.    
        ...#..v.
        .....#v.
        .#v<<<<.
        ..v...#.
The final password is still calculated from your final position and facing from the perspective of the map. In this example, the final row is 5, the final column is 7, and the final facing is 3, so the final password is 1000 * 5 + 4 * 7 + 3 = 5031.

Fold the map into a cube, then follow the path given in the monkeys' notes. What is the final password?
"""
def part2(input:Input)->str:
    grid,instructions, initial_state = read_initial_state(input)
    grid = wrap_cube(grid)
    # print_grid(grid)
    # print(instructions)
    # print(initial_state)
    final_state,path = walk(grid, instructions, initial_state)
    # print_grid(grid, path)

    return str(score_state(final_state))
