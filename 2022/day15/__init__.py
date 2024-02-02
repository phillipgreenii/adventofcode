from support import Input


from collections import namedtuple
Point = namedtuple('Point', 'x y')
Pair = namedtuple('Pair', 'sensor beacon')

# assumes format is "x=#, y=#"
def read_point(point_as_string):
    parts = point_as_string.split(",")
    x = int(parts[0].split("=")[1])
    y = int(parts[1].split("=")[1])
    return Point(x,y)

# assume format is Sensor at x=#, y=#: closest beacon is at x=#, y=#
def read_pairs(input:Input):
    for line in input.lines(skip_blanks=True):
        parts = line.split(":")
        sensor = read_point(parts[0][len('Sensor at'):])
        beacon = read_point(parts[1][len(' closest beacon is at'):])
        yield Pair(sensor,beacon)

import math
def distance(p1,p2):
    return abs(p1.x-p2.x) + abs(p1.y-p2.y)
    # return int(math.sqrt((p1.x-p2.x)**2 + (p1.y-p2.y)**2 ))

class Grid:
    def __init__(self, pairs):
        vals = {}
        distances = {}
        min_x = float('inf')
        max_x = float('-inf')
        min_y = float('inf')
        max_y = float('-inf')
        for sensor,beacon in pairs:
            vals[sensor] = 'S'
            vals[beacon] = 'B'
            d = distance(sensor,beacon)
            min_x = min(min_x,sensor.x-d,beacon.x)
            max_x = max(max_x,sensor.x+d,beacon.x)
            min_y = min(min_y,sensor.y-d,beacon.y)
            max_y = max(max_y,sensor.y+d,beacon.y)
            distances[sensor] = d

        self.values = vals
        self.distances = distances
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        # print(f"x:{min_x}->{max_x}: {max_x - min_x + 1}")
        # print(f"y:{min_y}->{max_y}: {max_y - min_y + 1}")

    def near_pair(self,p):
        for sensor,limit in self.distances.items():
        # for sensor,limit in [(Point(8,7),self.distances[Point(8,7)])]:
            d = distance(sensor,p)
            if d <= limit:
                return True
            
        return False

    def generate_line(self,y, window=None):
        if not window:
            window = [self.min_x, self.max_x]
        w_min_x, w_max_x = window
        line = []
        for x in range(w_min_x,w_max_x+1):
            # print(f"generating {x}")
            p = Point(x,y)
            v = self.values.get(p,'.')
            if v == '.' and self.near_pair(p):
                v = '#'
            line.append(v)     
        # print(f"len: {len(line)}")
        return line   

    def print(self, window=None):
        if not window:
            window = (self.min_x, self.max_x, self.min_y, self.max_y)

        w_min_x, w_max_x, w_min_y, w_max_y = window
        # print(f"window: {window}")
        
        x_labels = []
        for x in range(w_min_x,w_max_x+1):
            if x % 5 == 0:
                x_labels.append(str(x))
            else:
                x_labels.append('')
        x_len = max(map(len,x_labels))

        y_labels = []
        for y in range(w_min_y,w_max_y+1):
            y_labels.append(str(y))
        y_len = max(map(len,y_labels))

        for i in range(x_len):
            line = [' '] * (y_len+1)
            for x in x_labels:
                # if i >= len(x):
                #     line.append(' ')
                # else: 
                line.append(x.rjust(x_len)[i])
            print(''.join(line))            

        # x_digits = max(len(str(self.min_x)),len(str(self.max_x)))
        # x_goes_negative = self.min_x < 0
        # y_digits = max(len(str(abs(self.min_x))),len(str(abs(self.max_x))))

        for y in range(w_min_y,w_max_y+1):
            label = y_labels[y-w_min_y].rjust(y_len) + ' '
            line = self.generate_line(y, (w_min_x, w_max_x))
            # print(label + ''.join(line))


def part1(input:Input,y_to_check=2_000_000)->str:
    pairs = list(read_pairs(input))
    grid = Grid(pairs)
    # grid.print()
    # grid.print((-15,30,-15,30))
    # grid.print((-2,25,-2,22))
    # grid.print((-4,26,9,11))
    beacon_not_present = 0
    line = grid.generate_line(y_to_check)
    # print (len(line))
    # print( line )

    from collections import defaultdict
    counts = defaultdict(lambda :0)
    for v in line:
        counts[v] += 1
        if v == '#':
            beacon_not_present += 1

    # print(dict(counts))
    return str(beacon_not_present)

def calculate_frequency(point:Point)->int:
    return point.x * 4_000_000 + point.y 

def part2(input:Input, min_xy=0, max_xy=4_000_000)->str:
    pairs = list(read_pairs(input))
    grid = Grid(pairs)
    
    # FIXME implement determination of distress_signal
    distress_signal = Point(14,11)

    # print(distress_signal)
    return str(calculate_frequency(distress_signal))
