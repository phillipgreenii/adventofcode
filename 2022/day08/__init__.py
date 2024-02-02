from support import Input

class Tree:
    def __init__(self, height):
        self.height = height
        self.visible = False
        self.scenic_score = None

    def __repr__(self):
        return f"({self.height},{self.visible},{self.scenic_score})"

def load_grid(input:Input):
    grid = []
    for row in input.lines(skip_blanks=True):
        grid.append(list(map(lambda s: Tree(int(s)),list(row))))
        
    return grid

def mark_visible(grid):
   
    for row in grid:
        # walk left in each row
        max_height = -1
        for t in row:
            if t.height > max_height:
                t.visible = True
                max_height = t.height
            if max_height == 9:
                break
        # walk right in each row
        max_height = -1
        for t in row[::-1]:
            if t.height > max_height:
                t.visible = True
                max_height = t.height
            if max_height == 9:
                break

    row_count = len(grid)
    column_count = min(map(len,grid))
    for c in range(column_count):
        # walk down in each column
        max_height = -1
        for r in range(row_count):
            t = grid[r][c]
            if t.height > max_height:
                t.visible = True
                max_height = t.height
            if max_height == 9:
                break
        # walk up in each column
        max_height = -1
        for r in range(row_count-1,-1,-1):
            t = grid[r][c]
            if t.height > max_height:
                t.visible = True
                max_height = t.height
            if max_height == 9:
                break

def count_visible(grid):
    counter = 0
    for row in grid:
        for t in row:
            if t.visible:
                counter += 1
    return counter

def part1(input:Input)->str:
    grid = load_grid(input)

    mark_visible(grid)

    return str(count_visible(grid))

def calc_scenic_score(grid, row_count, column_count, r, c):
    height = grid[r][c].height
    # look left
    row = grid[r]
    left_count = 0
    for x in range(c-1,-1,-1):
        left_count += 1
        if row[x].height >= height:
            break
    # look right
    right_count = 0
    for x in range(c+1,column_count):
        right_count += 1
        if row[x].height >= height:
            break
    # look down
    down_count = 0
    for x in range(r+1,row_count):
        down_count += 1
        if grid[x][c].height >= height:
            break
    # look up
    up_count = 0
    for x in range(r-1, -1, -1):
        up_count += 1
        if grid[x][c].height >= height:
            break
    score = left_count * right_count * down_count * up_count 
    return score

def mark_scenic_score(grid):

    row_count = len(grid)
    column_count = min(map(len,grid))

    for r in range(row_count):
        for c in range(row_count):
            grid[r][c].scenic_score = calc_scenic_score(grid, row_count, column_count, r, c)


def find_max_scenic_score(grid):
    max_score = -1
    for row in grid:
        for t in row:
            max_score = max(t.scenic_score, max_score)
    return max_score

def part2(input:Input)->str:
    grid = load_grid(input)

    mark_scenic_score(grid)

    return str(find_max_scenic_score(grid))
