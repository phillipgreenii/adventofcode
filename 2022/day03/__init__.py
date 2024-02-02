from support import Input

def priortize_item(item):
    if ord('a') <= ord(item) and  ord(item) <= ord('z'):
        return ord(item) - ord('a') + 1
    elif  ord('A') <= ord(item) and  ord(item) <= ord('Z'):
        return ord(item) - ord('A') + 27
    else:
        raise f"Unknown item: {item}"

def part1(input:Input)->str:
    priority_sum = 0
    for line in input.lines(skip_blanks=True):
        firstpartitems, secondpartitems = set(line[:len(line)//2]), set(line[len(line)//2:])

        in_both = firstpartitems.intersection(secondpartitems)
        priority = priortize_item(next(iter(in_both)))

        priority_sum += priority
    
    return str(priority_sum)

def part2(input:Input)->str:
    priority_sum = 0
    elves = []
    for line in input.lines(skip_blanks=True):
        elves.append(line)
        if len(elves) < 3:
            continue

        in_all = set.intersection(*map(set,elves))
        elves = []
        priority = priortize_item(next(iter(in_all)))

        priority_sum += priority
    
    return str(priority_sum)
