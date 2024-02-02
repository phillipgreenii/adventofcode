from support import Input


from collections import namedtuple
Point = namedtuple('Point', 'x y')

def read_rock_paths(input:Input):
    def parse_line(line):
        return line.split("->")
    def parse_point(point):
        x,y = point.split(',')
        return Point(int(x),int(y))

    for line in input.lines(skip_blanks=True):
        yield tuple(map(parse_point, parse_line(line)))

def find_min_max(paths):
    min_x = paths[0][0].x
    max_x = paths[0][0].x
    min_y = paths[0][0].y
    max_y = paths[0][0].y

    for path in paths:
        for point in path:
            if point.x > max_x:
                max_x = point.x
            elif point.x < min_x:
                min_x = point.x
            if point.y > max_y:
                max_y = point.y
            elif point.y < min_y:
                min_y = point.y
    return min_x, max_x, min_y, max_y

OFF_GRID = Point(-1,-1)

class Cave:

    def __init__(self, min_x, max_x, min_y, max_y, floor_y):
        self.min_x, self.max_x, self.min_y, self.max_y, self.floor_y = min_x, max_x, min_y, max_y, floor_y
        self.values= dict()
        # height = max_y+1
        # width = max_x-min_x + 1        
        self.drop_point = None
        self.done = False

    def set_drop_point(self,point):
        self.drop_point = point
        self.draw_point(point, '+')

    def get_value(self, point):
        if self.floor_y and self.floor_y == point.y:
            return '#'
        return self.values.get(point, '.')

    def draw_point(self, point, value):
        self.min_x = min(point.x,self.min_x)
        self.max_x = max(point.x,self.max_x)
        # self.min_y = min(point.y,self.min_y)
        # self.max_y = max(point.y,self.max_y)
        self.values[point] = value

    def draw_path(self,path):
        # print(path)
        for i in range(len(path)-1):
            p1 = path[i]
            p2 = path[i+1]
            if p1.x == p2.x:
                # vertical
                start = min(p1.y, p2.y)
                end = max(p1.y, p2.y)
                # print(f"{start} => {end}")
                for y in range(start, end+1):
                    self.draw_point(Point(p1.x,y), '#')
            else:
                # horizontal
                start = min(p1.x, p2.x)
                end = max(p1.x, p2.x)
                # print(f"{start} => {end}")
                for x in range(start, end+1):
                    self.draw_point(Point(x,p1.y), '#')

    # returns the next move, None if no moves, 
    # OFF_GRID is a possible value 
    #  (this means no more should be dropped)
    def _determine_move(self, point):

        possible_moves = [
            Point(point.x, point.y+1),
            Point(point.x-1, point.y+1),
            Point(point.x+1, point.y+1),
        ]

        def is_out_of_bounds(p):
            return p.y > self.max_y or p.x > self.max_x or p.x < self.min_x

        for m in possible_moves:
            if not self.floor_y and is_out_of_bounds(m):
                return OFF_GRID
            elif self.floor_y and m.y == self.floor_y:
                continue
            else:
                v = self.get_value(m)
                if v == '.' or v == '+':
                    return m
        
        return None

    def drop_sand(self):
        if self.done:
            return False

        current = self.drop_point
        while True:
            # print('######')
            # print(current)
            new_p = self._determine_move(current)
            # print(new_p)

            if self.floor_y:
                if not new_p and current == self.drop_point:
                    self.done = True
                    break
            else:
                if new_p == OFF_GRID:
                    self.done = True
                    return False
            if new_p:
                current = new_p
            else: 
                break
        self.draw_point(current, 'o')
        return True
       

    def __repr__(self):
        lines = []
        if self.floor_y:
            upper_y = self.floor_y
        else: 
            upper_y = self.max_y
        for y in range(0, upper_y+1):
            line = []
            for x in range(self.min_x-1, self.max_x+1+1):
                line.append(self.get_value(Point(x,y)))
            lines.append("".join(line))

        return "\n".join(lines)

def build_cave(paths, add_floor=False):
    min_x, max_x, min_y, max_y = find_min_max(paths)
    # print(f"{min_x}, {max_x}, {min_y}, {max_y}")
    cave = Cave(min_x, max_x, min_y, max_y, max_y+2 if add_floor else None)
    for path in paths:
        cave.draw_path(path)
    cave.set_drop_point(Point(500,0))
    return cave

def part1(input:Input)->str:
    paths = list(read_rock_paths(input))
    cave = build_cave(paths)
    grains_dropped = 0
    while cave.drop_sand():
        grains_dropped += 1
    # print(cave)

    return str(grains_dropped)
    
def part2(input:Input)->str:
    paths = list(read_rock_paths(input))
    cave = build_cave(paths, True)
    grains_dropped = 0
    while cave.drop_sand():
        grains_dropped += 1
    # for _ in range(94):
    #     cave.drop_sand()
    # print(cave)

    return str(grains_dropped)
