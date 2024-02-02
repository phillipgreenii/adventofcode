from support import Input

def parse_elves(lines):
    elves = []
    current_count = 0
    for line in lines:
        if line == '':
            elves.append(current_count)
            current_count = 0
        else:
            current_count += int(line)
    elves.append(current_count)
    return elves

def part1(input:Input)->str:
    elves = parse_elves(input.lines())
    return str(max(elves))

def part2(input:Input)->str:
    elves = parse_elves(input.lines())
    elves.sort(reverse=True)
    return str(sum(elves[0:3]))
