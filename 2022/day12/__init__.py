from support import Input


def letter_to_height(letter):
    return ord(letter) - ord('a')

def read_map(input:Input):
    start = None
    goal = None
    grid = []
    for r,line in enumerate(input.lines(skip_blanks=True)):
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
    

def part1(input:Input)->str:
    (start,goal,grid) = read_map(input)
    graph = build_graph(grid)
    # for k,v in graph.items():
    #     print(f"{k}:{v}")
    path = find_dijkstra_min(start,goal,graph)

    # print(f"{path}")
    # minus one because the answer needed is steps, not total path size
    return str(len(path)-1)

def part2(input:Input)->str:
    # rushed for time on this one, a more efficient solution would have 
    # been to invert the graph and find the minimum from end to all starts.  
    # then iterate through all locations which start at 'a' and find the 
    # shortest.

    (start,goal,grid) = read_map(input)
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
    return str(min(map(len,paths))-1)
