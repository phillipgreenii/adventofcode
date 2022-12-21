
import re

from collections import deque

def init_stacks(stacks, line):
    stack_width = 4 #'[X] '
    i = 0
    while i < len(line):
        if line[i] == '[':
            stack_index = i//stack_width
            while len(stacks) <= stack_index:
                stacks.append(deque())
            stacks[stack_index].appendleft(line[i+1])
            i+= stack_width
        else:
            i+=1

def update_stacks_9000(stacks, line):
    parts = line.split()
    how_many = int(parts[1])
    from_index = int(parts[3])-1
    to_index = int(parts[5])-1

    for i in range(how_many):
        stacks[to_index].append(stacks[from_index].pop())    

def update_stacks_9001(stacks, line):
    parts = line.split()
    how_many = int(parts[1])
    from_index = int(parts[3])-1
    to_index = int(parts[5])-1
    tmp = deque(maxlen=how_many)

    for i in range(how_many):
        tmp.append(stacks[from_index].pop())
    while tmp:
        stacks[to_index].append(tmp.pop())

def determine_tops(stacks):
    tops = ''
    for s in stacks:
        if len(s) == 0:
            tops += ' '
        else:
            tops += s[-1]
    return tops

end_of_initial_state_line_contents = set('01234567890 ')

reading_initial_state = True
reading_movement = False
stacks_part1 = []
stacks_part2 = []
with open("input.txt", 'r') as file_in:
    for line in file_in:
        line = line.rstrip()
        if len(line) == 0:
            continue

        if set(line).issubset(end_of_initial_state_line_contents):
            reading_initial_state = False            

        if reading_initial_state:
            # hack, could parse once and duplicate, but went with this for now
            init_stacks(stacks_part1, line)
            init_stacks(stacks_part2, line)
        elif not reading_movement:
            # this skps the 1,2,3... line
            reading_movement = True
        else:
            update_stacks_9000(stacks_part1, line)
            update_stacks_9001(stacks_part2, line)
        



print("part 1")
# FCVRLMVQP

for s in stacks_part1:
    print(s)
print(determine_tops(stacks_part1))


print("part 2")
# RWLWGJGFD

for s in stacks_part2:
    print(s)
print(determine_tops(stacks_part2))