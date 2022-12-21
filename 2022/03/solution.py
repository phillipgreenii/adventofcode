

def priortize_item(item):
    if ord('a') <= ord(item) and  ord(item) <= ord('z'):
        return ord(item) - ord('a') + 1
    elif  ord('A') <= ord(item) and  ord(item) <= ord('Z'):
        return ord(item) - ord('A') + 27
    else:
        raise f"Unknown item: {item}"

priority_sum = 0
with open("input1.txt", 'r') as file_in:
    for line in file_in:
        line = line.strip()
        if len(line) == 0:
            continue

        firstpartitems, secondpartitems = set(line[:len(line)//2]), set(line[len(line)//2:])

        in_both = firstpartitems.intersection(secondpartitems)
        priority = priortize_item(next(iter(in_both)))

        # print(in_both)
        # print(priority)
        priority_sum += priority

print("part 1")
# 7553
print(priority_sum)

priority_sum = 0
elves = []
with open("input2.txt", 'r') as file_in:
    for line in file_in:
        line = line.strip()
        if len(line) == 0:
            continue

        elves.append(line)
        if len(elves) < 3:
            continue

        in_all = set.intersection(*map(set,elves))
        elves = []
        priority = priortize_item(next(iter(in_all)))

        # print(in_all)
        # print(priority)
        priority_sum += priority

print("part 2")
# 
print(priority_sum)