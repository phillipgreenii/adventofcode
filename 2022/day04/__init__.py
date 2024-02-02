from support import Input

def contains_completely(r1, r2):
    return r1[0] <= r2[0] and r2[1] <= r1[1]

def contains_partially(r1, r2):
    return (r1[0] <= r2[0] <= r1[1]) or (r1[0] <= r2[1] <= r1[1])

def find_overlaps(contains, input:Input)->int:
    c = 0
    for line in input.lines(skip_blanks=True):
        elves = line.split(',')
        r1 = tuple(map(int,elves[0].split('-')))
        r2 = tuple(map(int,elves[1].split('-')))
        if contains(r1,r2) or contains(r2,r1):
            c+=1
    return c

def part1(input:Input)->str:
    c = find_overlaps(contains_completely, input)
    return str(c)

def part2(input:Input)->str:
    c = find_overlaps(contains_partially, input)
    return str(c)
