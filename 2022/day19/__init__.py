from support import Input

from enum import Enum
from typing import NamedTuple, List, Iterator, Set, Dict, Optional

class Resource(Enum):
    ORE = 1
    CLAY = 2
    OBSIDIAN = 3
    GEODE = 4

class Cost(NamedTuple):
    unit:int
    resource:Resource

# class RobotRecipe(NamedTuple):
#     type:Resource
#     cost:Cost

class BluePrint(NamedTuple):
    id:int
    recipes:Dict[Resource,List[Cost]]

def print_blue_print(blue_print):
    print(f"Blue Print {blue_print.id}")
    for r,cs in blue_print.recipes.items():
        cost = ", ".join([f"{c.unit} {c.resource.name}" for c in cs])
        print(f"\t{r.name} Robot: {cost}")

def read_blue_prints(input:Input) -> Iterator[BluePrint]:
    for line in input.lines(skip_blanks=True):
        parts = line.split(':')
        id = int(parts[0][10:])
        parts = parts[1].split('.')
        recipes:Dict[Resource,List[Cost]] = dict()
        for recipe in parts:
            if recipe == '':
                continue
            r_parts = recipe.split("robot")
            type_str = r_parts[0].split(' ')[3].upper()
            type = Resource[type_str]
            c_parts = r_parts[1][7:].split('and')
            costs = []
            for c_part in c_parts:
                cp = c_part.strip().split(' ')
                u = int(cp[0])
                r_s = cp[1].upper()
                r = Resource[r_s]
                costs.append(Cost( u,r))
            recipes[type] = costs
        yield BluePrint(id,recipes)

class State(NamedTuple):
    time_remaining:int
    # building:Optional[Resource]
    robots:Dict[Resource,int]
    resources:Dict[Resource,int]

class Searcher:

    def __init__(self,blue_print:BluePrint):
        self.blue_print = blue_print
        self.solutions = []

    def _tick(self,old_state:State,robot_to_purchase:Optional[Resource]=None)->State:
        # print(f"ticking {old_state},{robot_to_purchase}")
        
        # buy
        resources = old_state.resources.copy()
        if robot_to_purchase:
            for c in self.blue_print.recipes[robot_to_purchase]:
                resources[c.resource] -= c.unit
    
        # collect
        for r,n in old_state.robots.items():
            if r not in resources:
                resources[r] = 0
            resources[r] += n

        # build
        robots = old_state.robots   
        if robot_to_purchase:
            n = 0 if robot_to_purchase not in old_state.robots else old_state.robots[robot_to_purchase]
            n += 1
            robots = {**robots,robot_to_purchase:n}
    
        return State(old_state.time_remaining-1,robots,resources)

    def _next_moves(self,state:State)->List[State]:
        if state.time_remaining == 0:
            return []

        # no purchase
        moves = [self._tick(state)]

        # one per purchase
        for r,cs in self.blue_print.recipes.items():
            can_buy = True
            for c in cs:
                if c.resource not in state.resources or state.resources[c.resource] < c.unit:
                    can_buy = False
                    break
            if can_buy:
                moves.append(self._tick(state,robot_to_purchase =r))

        return moves

    def _search(self, current_state:State):
        for m in self._next_moves(current_state):
            if m.time_remaining == 0:
                # print(f"adding {m}")
                self.solutions.append(m)
            else:
                self._search(m)

    def find_max_geodes(self, max_minutes):
        initial_state = State(max_minutes,{Resource.ORE:1},{})
        self._search(initial_state)
        print(f"solution count: {self.solutions}")

        return max(self.solutions, key=lambda s:s.resources[Resource.GEODE])


def determine_max_geodes(blue_print:BluePrint, minutes:int):
    return Searcher(blue_print).find_max_geodes(minutes)

def part1(input:Input)->str:
    total_quality_level = 0
    for blue_print in read_blue_prints(input):
        print_blue_print(blue_print)
        max_geodes = determine_max_geodes(blue_print, 24)
        quality_level = max_geodes * blue_print.id
        print(f"{blue_print.id}*{max_geodes}={quality_level}")
        total_quality_level += quality_level
    return str(total_quality_level)
