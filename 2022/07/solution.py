
import re

from collections import deque

def find_first_unique_set_of_size(size, signal):
    for i in range(size-1, len(signal)):
        window = signal[(i-size):i]
        # print(window)
        uniq_symbols = set(window)
        # print(uniq_symbols)
        if len(uniq_symbols) == size:
            return i
    return None

def find_signal_start(signal):
    return find_first_unique_set_of_size(4, signal)

def find_message_start(signal):
    return find_first_unique_set_of_size(14, signal)

def read_lines(file_name):
    with open(file_name, 'r') as file_in:
        for line in file_in:
            line = line.rstrip()
            if len(line) == 0:
                continue

            yield line

def parse_lines(lines):
    for line in lines:
        parts = line.split()
        if parts[0] == '$':
            yield tuple(['command']+parts[1:])
        elif parts[0] == 'dir':
            yield tuple(parts)
        else:
            yield tuple(['file',parts[1], parts[0]])

def parse_fs(file_name):
    fs = dict()
    prev_dirs = deque()
    current_dir = fs
    prev_dirs.append(current_dir)
    for line in parse_lines(read_lines(file_name)):
        # print("###########")
        # print(line)
        # print(prev_dirs)
        # print(current_dir)
        type = line[0]
        if type == 'command':
            command = line[1]
            if command == 'cd':
                dir_name = line[2]
                if dir_name == '/':
                    current_dir = fs
                elif dir_name == '..':
                    current_dir = prev_dirs.pop()
                else:
                    prev_dirs.append(current_dir)
                    current_dir = current_dir[dir_name]
            elif command == 'ls':
                pass
            else:
                raise Exception(f"Unknown command: {command}")
        elif type == 'dir':
            dir_name = line[1]
            current_dir[dir_name] = dict()
        elif type == 'file':
            file_name = line[1]
            file_size = int(line[2])
            current_dir[file_name] = file_size
        # print(prev_dirs)
        # print(current_dir)
        # print()
    return fs

def sum_dir(current_dir):
    sums = dict({'.':0})
    # print(current_dir)
    for name,data in current_dir.items():
        # print(name)
        # print(data)
        if isinstance(data, int):
            sums['.'] += data
        else:
            r = sum_dir(data)
            sums[name] = r
            sums['.'] += r['.']
    return sums

def sum_small_dirs(dir_sums, limit):
    # print("######")
    # print(dir_sums)
    # print(limit)
    total = 0
    for name, data in dir_sums.items():
        if isinstance(data, int):
            if data <= limit:
                total += data
        else:
            total += sum_small_dirs(dir_sums[name], limit)
    # print(total)
    return total

def run_part1(file_name):
    fs = parse_fs(file_name)
    dir_sums = sum_dir(fs)
        
    # print(fs)
    # print(dir_sums)
    return sum_small_dirs(dir_sums, 100_000)

def find_matching_dirs(dir_sums, predicate):
    sizes = set()
    # print('#####')
    # print(sizes)
    for name, data in dir_sums.items():
        if isinstance(data, int):
            if predicate(data):
                sizes.add(data)
        else:
            sizes = sizes.union(find_matching_dirs(dir_sums[name], predicate))
    # print(sizes)
    return sizes

def run_part2(file_name):
    total_fs_space = 70_000_000
    required_fs_space = 30_000_000
    max_usable_fs_space = total_fs_space - required_fs_space

    fs = parse_fs(file_name)
    dir_sums = sum_dir(fs)
    
    goal_fs_space = dir_sums['.'] - max_usable_fs_space
    # print(goal_fs_space)
    
    # print(dir_sums)
    candidates = find_matching_dirs(dir_sums, lambda x: x>= goal_fs_space)
    # candidates = find_matching_dirs(dir_sums, lambda x: True)
    # print(candidates)
    
    
    return min(candidates)
    # print(fs)
    # print(dir_sums)
    # return sum_small_dirs(dir_sums, 100_000)

print("part 1")
# 95437
print(run_part1('example.txt'))
# 1611443
print(run_part1('input.txt'))

print("part 2")
# 24933642
print(run_part2('example.txt'))
# 2086088
print(run_part2('input.txt'))
