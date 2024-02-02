from support import Input

from collections import deque

def parse_lines(lines):
    for line in lines:
        parts = line.split()
        if parts[0] == '$':
            yield tuple(['command']+parts[1:])
        elif parts[0] == 'dir':
            yield tuple(parts)
        else:
            yield tuple(['file',parts[1], parts[0]])

def parse_fs(input:Input):
    fs = dict()
    prev_dirs = deque()
    current_dir = fs
    prev_dirs.append(current_dir)
    for line in parse_lines(input.lines(skip_blanks=True)):
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
    return fs

def sum_dir(current_dir):
    sums = dict({'.':0})
    for name,data in current_dir.items():
        if isinstance(data, int):
            sums['.'] += data
        else:
            r = sum_dir(data)
            sums[name] = r
            sums['.'] += r['.']
    return sums

def sum_small_dirs(dir_sums, limit):
    total = 0
    for name, data in dir_sums.items():
        if isinstance(data, int):
            if data <= limit:
                total += data
        else:
            total += sum_small_dirs(dir_sums[name], limit)
    return total

def part1(input:Input)->str:
    fs = parse_fs(input)
    dir_sums = sum_dir(fs)
        
    return str(sum_small_dirs(dir_sums, 100_000))

def find_matching_dirs(dir_sums, predicate):
    sizes = set()
    for name, data in dir_sums.items():
        if isinstance(data, int):
            if predicate(data):
                sizes.add(data)
        else:
            sizes = sizes.union(find_matching_dirs(dir_sums[name], predicate))

    return sizes

def part2(input:Input)->str:
    total_fs_space = 70_000_000
    required_fs_space = 30_000_000
    max_usable_fs_space = total_fs_space - required_fs_space

    fs = parse_fs(input)
    dir_sums = sum_dir(fs)
    
    goal_fs_space = dir_sums['.'] - max_usable_fs_space

    candidates = find_matching_dirs(dir_sums, lambda x: x>= goal_fs_space)
   
    return str(min(candidates))
