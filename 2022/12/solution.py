def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

def letter_to_height(letter):
    return ord(letter) - ord('a')

def read_map(file_name):
    start = None
    goal = None
    grid = []
    for r,line in enumerate(read_lines(file_name)):
        row = []
        grid.append(row)
        for c, letter in enumerate(line):
            if letter == 'S':
                start = (r,c)
                row.append(letter_to_height('a'))
            elif letter == 'E':
                goal = (r,c)
                row.append(letter_to_height('z'))
            else:
                row.append(letter_to_height(letter))

    return (start, goal, grid)

# from dataclasses import dataclass, field
# from typing import Any


# def generate_uuid():
#     x = 0
#     while x < 10_000:
#         yield x
#         x += 1
#     raise Exception("too many paths")

# UUID = generate_uuid()

# @dataclass(order=True)
# class Path:
#     id: int=field(compare=False)
#     step_count: int
#     steps: Any=field(compare=False)

#     def __init__(self, steps):
#         self.id = next(UUID)
#         # checked = set(start)
#         self.steps = steps
#         self.step_count = len(steps)-1

#     def __repr__(self):
#         return f"P[{self.id}]:{self.position()}:{self.step_count}"

#     def contains(self, position):
#         return position in self.steps

#     def position(self):
#         return self.steps[-1]

#     def append(self, position):
#         return Path(self.steps + [position])


def find_valid_moves(position, grid):

    possible_moves = [ 
        # down
        (position[0]+1, position[1]),
        # up
        (position[0]-1, position[1]),
        # right
        (position[0], position[1] + 1),
        # left
        (position[0], position[1] - 1),
    ]

    height = grid[position[0]][position[1]]
    moves = []
    for m in possible_moves:
        (r,c) = m

        if 0 <= r < len(grid) \
            and 0 <= c < len(grid[r]) \
            and grid[r][c] <= height + 1:
            moves.append(m)

    return moves

import heapq

# def find_path(start,goal, grid):
#     paths = []
#     def push(path):
#         # heapq.heappush(paths,(path.step_count(),path))
#         heapq.heappush(paths,path)
#     def pop():
#         return heapq.heappop(paths)
#         # _,path = heapq.heappop(paths)
#         # return path
#     push(Path([start]))
#     while paths:
#         print(f"paths size:{len(paths)}")
#         print(f"top paths:{[p.step_count for p in paths][:10]} ")
#         path = pop()
#         print(f"c?: {path.contains(start)}")
#         print(f"paths size:{len(paths)}")
#         print(f"{path}")
#         moves = find_valid_moves(path.position(), grid)
#         for m in moves:
#             print(f'trying {m}')
#             if not path.contains(m):
#                 print(f'appending {m} to {path}')
#                 p =  path.append(m)                
#                 if p.contains(goal):
#                     return p
#                 push(p)
#     return None


# def part1_old(file_name):
#     (start, goal, grid) = read_map(file_name)

#     # print(start)
#     # print(goal)
#     # for r in grid:
#     #     print(''.join(map(lambda h: f"{h:3}",r)))

#     path = find_path(start,goal, grid)
#     # print(path.steps)

#     return path.step_count

# from based on https://github.com/abecus/DS-and-Algorithms/blob/master/graph/dijkstra.py
import collections
def find_dijkstra_min(start,goal,graph):
    seen = set()
    parents_map = dict()
    pq = []
    node_costs = collections.defaultdict(lambda: float('inf'))
    node_costs[start] = 0
    heapq.heappush(pq, (0, start))
    while pq:
		# go greedily by always extending the shorter cost nodes first
        _, node = heapq.heappop(pq)
        seen.add(node)
 
        for neighbor in graph[node]:
            if neighbor in seen:
                continue
				
            cost = node_costs[node] + 1
            if node_costs[neighbor] > cost:
                parents_map[neighbor] = node
                node_costs[neighbor] = cost
                heapq.heappush(pq, (cost, neighbor))
    
    # print('parents')
    # for k,v in parents_map.items():
    #     print(f"{k}:{v}")
    next_node = goal
    path = []
    while next_node:
        path.append(next_node)
        next_node = parents_map.get(next_node,None)        
        
    if len(path) == 1:
        return None
    else:
        return path[::-1]

def build_graph(grid):
    g = dict()

    for r,row in enumerate(grid):
        for c,_ in enumerate(row):
            g[(r,c)] = find_valid_moves((r,c), grid)

    return g
    

def part1(file_name):
    (start,goal,grid) = read_map(file_name)
    graph = build_graph(grid)
    # for k,v in graph.items():
    #     print(f"{k}:{v}")
    path = find_dijkstra_min(start,goal,graph)

    # print(f"{path}")
    # minus one because the answer needed is steps, not total path size
    return len(path)-1

def part2(file_name):
    # rushed for time on this one, a more efficient solution would have 
    # been to invert the graph and find the minimum from end to all starts.  
    # then iterate through all locations which start at 'a' and find the 
    # shortest.

    (start,goal,grid) = read_map(file_name)
    graph = build_graph(grid)

    paths = []
    for r,row in enumerate(grid):
        for c, height in enumerate(row):
            if height == 0:
                # print(f"running: ({r},{c})")
                path = find_dijkstra_min((r,c),goal,graph)
                if path:
                    paths.append(path)

    # for p in paths:
    #     print(f"{p[0]}:{len(p)-1}")

    # print('xxx')
    # print(len(paths))

    # print(f"{path}")
    # minus one because the answer needed is steps, not total path size
    return min(map(len,paths))-1


print("part 1")
# 31
print(part1('example.txt'))
# 437
print(part1('input.txt'))

print("part 2")
# 29
print(part2('example.txt'))
# 457
print(part2('input.txt'))