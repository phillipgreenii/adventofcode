
elves = []
current_count = 0
last_line = None
with open("input.txt", 'r') as file_in:
    for line in file_in:
        line = line.strip()
        # print(line)

        last_line = line
        if line == '':
            elves.append(current_count)
            current_count = 0
        else:
            current_count += int(line)
    elves.append(current_count)

# print(elves)
# print(last_line)
# print(lines)
print("part 1")
print(max(elves))


print("part 2")
elves.sort(reverse=True)
print(elves[0:3])