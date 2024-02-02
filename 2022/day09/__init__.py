from support import Input

def read_moves(input:Input):
    for line in input.lines(skip_blanks=True):
        direction, spaces = line.split()
        spaces = int(spaces)
        yield (direction, spaces)

def move_head(h, direction):
    if direction == 'R':
        return (h[0]+1, h[1])
    if direction == 'L':
        return (h[0]-1, h[1])
    if direction == 'U':
        return (h[0], h[1]+1)
    if direction == 'D':
        return (h[0], h[1]-1)
    raise Exception(f"Unknown Direction: {direction}")

def close_enough(h,t):
    # close enough:
    #    sqrt(2)  >= sqrt( (x2-x1)^2 +(y2-y1)^2 )
    #    2  >= (x2-x1)^2 +(y2-y1)^2 
    # don't need to worry about  exponent, if delta x is <= 1 and delta y <= 1, then good
    return (h == t) \
        or ( (abs(h[0]-t[0]) <= 1) and (abs(h[1]-t[1]) <= 1) )

def move_tail(t, h):
    if close_enough(h,t):
        return t
    # same x (move N/S)
    if t[0] == h[0]:
        if t[1] < h[1]:
            return (t[0], t[1]+1)
        else: 
            return (t[0], t[1]-1)
    # same y (move E/W)
    if t[1] == h[1]:
        if t[0] < h[0]:
            return (t[0]+1, t[1])
        else: 
            return (t[0]-1, t[1])
    # move NW
    if t[0] < h[0] and t[1] < h[1]:
        return (t[0]+1, t[1]+1)
    # move SW
    if t[0] > h[0] and t[1] < h[1]:
        return (t[0]-1, t[1]+1)
    # move NE
    if t[0] < h[0] and t[1] > h[1]:
        return (t[0]+1, t[1]-1)    
    # move SE
    if t[0] > h[0] and t[1] > h[1]:
        return (t[0]-1, t[1]-1)
    # WRONG
    raise Exception(f"BAD: h={h}; t={t}")

def xy2rc(c,max):
    return (c[1],c[0])

def print_rope(h, t, max=6):
    pass
    # print(f"h={h};t={t}")
    # grid = [ ['.'] * max for _ in range(max)]
    # rc_s = xy2rc((0,0),max)
    # grid[rc_s[0]][rc_s[1]]='s'
    # rc_t = xy2rc(t,max)
    # grid[rc_t[0]][rc_t[1]] = 'T'
    # rc_h = xy2rc(h,max)
    # grid[rc_h[0]][rc_h[1]] = 'H'
    # # print(grid)
    # # print()
    # for row in grid[::-1]:
    #     print(''.join(row))


def part1(input:Input)->str:
    visited_positions = set()

    #   (x,y)
    h = (0,0)
    t = (0,0)

    visited_positions.add(t)    
    # print_rope(h,t)
    for move in read_moves(input):
        for _ in range(move[1]):
            h = move_head(h, move[0])
            t = move_tail(t, h)
            visited_positions.add(t)
            # print_rope(h,t)

    return str(len(visited_positions))

def part2(input:Input)->str:
    visited_positions = set()

    #   (x,y)
    chain = [ (0,0) for _ in range(10)]    

    visited_positions.add(chain[-1])
    # print_rope(h,t)
    for move in read_moves(input):
        # print(f"{move}")
        for _ in range(move[1]):
            chain[0] = move_head(chain[0], move[0])
            for i in range(1,len(chain)):
                chain[i] = move_tail(chain[i], chain[i-1])
            visited_positions.add(chain[-1])
            # print_rope(h,t)

    return str(len(visited_positions))
