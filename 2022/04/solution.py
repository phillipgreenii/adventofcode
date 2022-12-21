

def contains_completely(r1, r2):
    return r1[0] <= r2[0] and r2[1] <= r1[1]

def contains_partially(r1, r2):
    return (r1[0] <= r2[0] <= r1[1]) or (r1[0] <= r2[1] <= r1[1])

complete_overlap_count = 0
partial_overlap_count = 0
with open("input.txt", 'r') as file_in:
    for line in file_in:
        line = line.strip()
        if len(line) == 0:
            continue
        elves = line.split(',')
        r1 = tuple(map(int,elves[0].split('-')))
        r2 = tuple(map(int,elves[1].split('-')))
        complete_overlap = contains_completely(r1,r2) or contains_completely(r2,r1)
        partial_overlap =  contains_partially(r1,r2) or contains_partially(r2,r1)
        # print(r1)
        # print(r2)
        # print(complete_overlap)
        if complete_overlap:
            complete_overlap_count+=1
        if partial_overlap:
            partial_overlap_count+=1

print("part 1")
# 573
print(complete_overlap_count)

print("part 2")
# 867
print(partial_overlap_count)