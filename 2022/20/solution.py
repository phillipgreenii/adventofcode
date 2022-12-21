def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

def read_code(file_name:str):
    return list(map(int,read_lines(file_name)))

def part1(file_name):
    code = read_code(file_name)
    print(code)
    
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

print("part 1")
# 4,-3,2 -> 3
print(part1('example.txt'))
# 3068
# print(part1('input.txt'))

# print("part 2")
# # 93
# print(part2('example.txt'))
# # 23958
# print(part2('input.txt'))