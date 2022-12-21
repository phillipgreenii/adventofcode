def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

from collections import namedtuple
Valve = namedtuple('Valve', 'id rate leads')

# assume line looks like
# Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
def parse_valve(line):
    # print('XXXX')
    halves = line.split(';')
    # print(halves)
    parts = halves[0].split()
    # print(parts)
    id = parts[1]
    rate = int(parts[-1].split('=')[1])
    leads = list(map(lambda x: x.rstrip(','),halves[1].split()[4:]))
    return Valve(id,rate,leads)


def read_valves(file_name):
    for line in read_lines(file_name):
        yield parse_valve(line)

State = namedtuple('State', 'position remaining_valves pressure_output released_pressure time_remaining')

import heapq



# from based on https://github.com/abecus/DS-and-Algorithms/blob/master/graph/dijkstra.py
import collections
def find_dijkstra_shortest_paths(start,graph):
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
    paths = {}

    for goal in graph.keys():
        if goal == start:
            continue
        next_node = goal
        path = []

        while next_node:
            path.append(next_node)
            next_node = parents_map.get(next_node,None)  
        # remove reference to start node from path
        path = path[:-1]  
        # reverse
        paths[goal] = path[::-1]    
        
    return paths

def build_graph(valves):
    g = dict()

    for v in valves.values():
        g[v.id] = v.leads

    return g


class Searcher:

    def __init__(self,valves):
        self.valves = valves
        self.solutions = []
        self.shortest_paths = {}
        self.graph = build_graph(valves)

    def _build_shortest_paths(self,origin):
        return find_dijkstra_shortest_paths(origin,self.graph)

    def _navigate(self,origin,destination):
        if origin not in self.shortest_paths:
            self.shortest_paths[origin] = self._build_shortest_paths(origin)
        return self.shortest_paths[origin][destination]

    def _tick(self,old_state,new_position=None, open_valve=None):
        # print(f"{old_state}->{new_position}|{open_valve}")
        if bool(new_position) and  bool(open_valve):
            raise Exception("both new_position and open_value can't be specified")
        if new_position is None and open_valve is None:
            return State(
                position=old_state.position,
                remaining_valves=old_state.remaining_valves,
                pressure_output = old_state.pressure_output,
                released_pressure= old_state.pressure_output+old_state.released_pressure, 
                time_remaining = old_state.time_remaining -1)
        if new_position is not None:
            if new_position == old_state.position:
                raise Exception(f"Cannot move to same position: {new_position}")
            return State(
                position=new_position, 
                remaining_valves = old_state.remaining_valves, 
                pressure_output = old_state.pressure_output,
                released_pressure= old_state.pressure_output+old_state.released_pressure, 
                time_remaining = old_state.time_remaining -1)
        if open_valve is not None:
            if open_valve  not in old_state.remaining_valves:
                raise Exception(f"Cannot open if already open: {open_valve}")
            remaining_valves = set(old_state.remaining_valves)
            remaining_valves.remove(open_valve) 
            pressure_output = old_state.pressure_output + self.valves[open_valve].rate

            return State(
                position=old_state.position, 
                remaining_valves = remaining_valves, 
                pressure_output =pressure_output,
                released_pressure= pressure_output+old_state.released_pressure, 
                time_remaining = old_state.time_remaining -1)

    def _next_moves(self,state):
        if state.time_remaining == 0:
            return []
        # print(f"{state.position} in {state.remaining_valves}?")
        if state.position in state.remaining_valves:
            state = self._tick(state, open_valve=state.position)
            if state.time_remaining == 0:
                return [state]

        if len(state.remaining_valves) == 0:
            while state.time_remaining > 0:
                state = self._tick(state)
            return [state]

        moves = []
        for next_position in state.remaining_valves:
            path = self._navigate(state.position, next_position)
            s = state
            for n in path:
                s = self._tick(s,new_position=n)
                if s.time_remaining == 0:
                    break
            moves.append(s)
        return moves


    def _search(self, current_state):
        for m in self._next_moves(current_state):
            if m.time_remaining == 0:
                self.solutions.append(m)
            else:
                self._search(m)

    def find_max_pressure_release(self, max_minutes, starting_valve_id):

        remaining_valves = set([v.id for v in self.valves.values() if v.rate >0])
        self._search(State(self.valves[starting_valve_id].id, remaining_valves, 0, 0, max_minutes-1 ))

        return max(self.solutions, key=lambda s:s.released_pressure)


def part1(file_name):
    valves = {v.id:v  for v in read_valves(file_name)}
    # print(valves)
    # for k,v in valves.items():
    #     print(v)

    searcher = Searcher(valves)

    mpr = searcher.find_max_pressure_release(30, 'AA')
    print(mpr)
    # print("###############")
    # for s in searcher.solutions:
    #     print(s)
    return mpr.released_pressure
    
def part2(file_name):
    valves = {v.id:v  for v in read_valves(file_name)}
    # print(valves)
    # for k,v in valves.items():
    #     print(v)

    searcher = Searcher(valves)

    mpr = searcher.find_max_pressure_release(30, 'AA')
    print(mpr)
    # print("###############")
    # for s in searcher.solutions:
    #     print(s)
    return mpr.released_pressure
    
"""
You're worried that even with an optimal approach, the pressure released won't be enough. What if you got one of the elephants to help you?

It would take you 4 minutes to teach an elephant how to open the right valves in the right order, leaving you with only 26 minutes to actually execute your plan. Would having two of you working together be better, even if it means having less time? (Assume that you teach the elephant before opening any valves yourself, giving you both the same full 26 minutes.)

In the example above, you could teach the elephant to help you as follows:

== Minute 1 ==
No valves are open.
You move to valve II.
The elephant moves to valve DD.

== Minute 2 ==
No valves are open.
You move to valve JJ.
The elephant opens valve DD.

== Minute 3 ==
Valve DD is open, releasing 20 pressure.
You open valve JJ.
The elephant moves to valve EE.

== Minute 4 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve II.
The elephant moves to valve FF.

== Minute 5 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve AA.
The elephant moves to valve GG.

== Minute 6 ==
Valves DD and JJ are open, releasing 41 pressure.
You move to valve BB.
The elephant moves to valve HH.

== Minute 7 ==
Valves DD and JJ are open, releasing 41 pressure.
You open valve BB.
The elephant opens valve HH.

== Minute 8 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You move to valve CC.
The elephant moves to valve GG.

== Minute 9 ==
Valves BB, DD, HH, and JJ are open, releasing 76 pressure.
You open valve CC.
The elephant moves to valve FF.

== Minute 10 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant moves to valve EE.

== Minute 11 ==
Valves BB, CC, DD, HH, and JJ are open, releasing 78 pressure.
The elephant opens valve EE.

(At this point, all valves are open.)

== Minute 12 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 20 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.

...

== Minute 26 ==
Valves BB, CC, DD, EE, HH, and JJ are open, releasing 81 pressure.
With the elephant helping, after 26 minutes, the best you could do would release a total of 1707 pressure.

With you and an elephant working together for 26 minutes, what is the most pressure you could release?
"""
print("part 1")
# 1651
print(part1('example.txt'))
# 2124
print(part1('input.txt'))

print("part 2")
# 1707
print(part2('example.txt'))
# ?
# print(part2('input.txt'))