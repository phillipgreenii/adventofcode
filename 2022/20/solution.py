def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

def read_code(file_name:str):
    return list(map(int,read_lines(file_name)))

def wrap_position(max_len, pos):
    p = (pos+max_len-1) % (max_len-1)
    if p == 0:
        p = max_len-1
    return p



def test_wrap_position():
    max_len = 7
    tests = [
        (-6  ,6),
        (0   ,6),
        (6   ,6),
        (-1  ,5),
        (5   ,5),
        (1   ,1),
        (3+ 1,4),
        (1+-2,5)
    ]

    for p,ev in tests:
        v = wrap_position(max_len,p)
        if v != ev:
            raise Exception(f"{v} != {ev}")
    
#  -6/0/6:  4,  X,  5,  6,  7,  8, 9,
#    -1/5:  X, -4,  5,  6,  7,  8, 9,
#    -2/4: -4,  5,  6,  7,  8,  X, 9,
#    -3/3: -4,  5,  6,  7,  X,  8, 9, 
#    -4/2: -4,  5,  6,  X,  7,  8, 9, 
#    -5/1: -4,  5,  X,  6,  7,  8, 9, 

def rotate(l,x):
    # if x == 0:
    #     return
    pos = l.index(x)
    new_pos = wrap_position(len(l), pos+x)
    # new_pos = (pos + x + len(l)) % len(l)
    # print(f"move {x} from {pos} to {new_pos}")
    l.pop(pos)
    l.insert(new_pos,x)

def test_rotate():
    print("Test rotate()")
    tests = [
        ([ 1,  2, -3,  3, -2,  0,  4], 1,[ 2,  1, -3,  3, -2,  0,  4]),
        ([ 2,  1, -3,  3, -2,  0,  4], 2,[ 1, -3,  2,  3, -2,  0,  4]),
        ([ 1, -3,  2,  3, -2,  0,  4],-3,[ 1,  2,  3, -2, -3,  0,  4]),
        ([ 1,  2,  3, -2, -3,  0,  4], 3,[ 1,  2, -2, -3,  0,  3,  4]),
        ([ 1,  2, -2, -3,  0,  3,  4],-2,[ 1,  2, -3,  0,  3,  4, -2]),
        ([ 1,  2, -3,  0,  3,  4, -2], 0,[ 1,  2, -3,  0,  3,  4, -2]),
        ([ 1,  2, -3,  0,  3,  4, -2], 4,[ 1,  2, -3,  4,  0,  3, -2]),
    ]

    success = 0
    for l,x,expected_result in tests:
        rotate(l,x)
        if l != expected_result:
            raise Exception(f"{x}: {l} != {expected_result}")
        success += 1
    print(f"Success: {success}/{len(tests)}")
    


def extract_coordinates(code, offsets):
    zero_pos = code.index(0)
    # return [ code[wrap_position(len(code),zero_pos+offset)] for offset in offsets ]
    return [ code[(zero_pos+offset)%len(code)] for offset in offsets ]

def part1(file_name):
    original_code = read_code(file_name)
    code = list(original_code)
    print(code)
    for x in original_code:
        # pos = code.index(x)
        rotate(code,x)
        # print(code)
        # print()

    print(code)
    
    print(wrap_position(len(code),1+-2))
    cooridinates = extract_coordinates(code, [1000,2000,3000] )
    print(cooridinates)
    return sum(cooridinates)
    
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

test_wrap_position()
test_rotate()

print("part 1")
# 4,-3,2 -> 3
print(part1('example.txt'))
# -77, -8178, -7203 -> -15458
print(part1('input.txt'))

# print("part 2")
# # 93
# print(part2('example.txt'))
# # 23958
# print(part2('input.txt'))