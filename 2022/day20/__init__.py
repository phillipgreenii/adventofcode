from support import Input

def read_code(input:Input):
    return list(map(int,input.lines(skip_blanks=True)))

def wrap_position(max_len, pos):
    p = (pos+max_len-1) % (max_len-1)
    if p == 0:
        p = max_len-1
    return p

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

def extract_coordinates(code, offsets):
    zero_pos = code.index(0)
    # return [ code[wrap_position(len(code),zero_pos+offset)] for offset in offsets ]
    return [ code[(zero_pos+offset)%len(code)] for offset in offsets ]

def part1(input:Input)->str:
    original_code = read_code(input)
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
    return str(sum(cooridinates))
