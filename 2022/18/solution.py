def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

from typing import NamedTuple, List, Iterator, Set

class LavaDroplet(NamedTuple):
    x:int
    y:int
    z:int

def read_droplets(file_name) -> Iterator[LavaDroplet]:
    for line in read_lines(file_name,skip_blanks=False):
        parts = line.split(',')
        yield LavaDroplet(int(parts[0]),int(parts[1]), int(parts[2]))

def generate_neighbors(droplet:LavaDroplet) -> Set[LavaDroplet]:
    return set([
        LavaDroplet(droplet.x+1,droplet.y,droplet.z),
        LavaDroplet(droplet.x-1,droplet.y,droplet.z),
        LavaDroplet(droplet.x,droplet.y+1,droplet.z),
        LavaDroplet(droplet.x,droplet.y-1,droplet.z),
        LavaDroplet(droplet.x,droplet.y,droplet.z+1),
        LavaDroplet(droplet.x,droplet.y,droplet.z-1)
    ])

def part1(file_name):
    droplets = set(read_droplets(file_name))

    # print(droplets)

    exposed_faces = 0
    for d in droplets:
        ef = 0
        for n in generate_neighbors(d):
            if n not in droplets:
                ef += 1
        exposed_faces += ef


    return exposed_faces

def find_exterior_droplets(droplets):
    min_x = float('inf')
    min_y = float('inf')
    min_z = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')
    max_z = float('-inf')
    for d in droplets:
        min_x = min(min_x,d.x)
        max_x = max(max_x,d.x)
        min_y = min(min_y,d.y)
        max_y = max(max_y,d.y)
        min_z = min(min_z,d.z)
        max_z = max(max_z,d.z)
    # print(min_x)
    # print(max_x)
    # print(min_y)
    # print(max_y)
    # print(min_z)
    # print(max_z)
    exterior_droplets = set()
    # print(f"Total Volume: {(max_x-min_x+1)*(max_y-min_y+1)*(max_z-min_z+1)}")

    q = [
        LavaDroplet(max_x+1,max_y+1,max_z+1),
        LavaDroplet(max_x+1,max_y+1,min_z-1),
        LavaDroplet(max_x+1,min_y-1,max_z+1),
        LavaDroplet(min_x-1,max_y+1,max_z+1),
        LavaDroplet(min_x-1,min_y-1,max_z+1),
        LavaDroplet(max_x+1,min_y-1,min_z-1),
        LavaDroplet(min_x-1,max_y+1,min_z-1),
        LavaDroplet(min_x-1,min_y-1,min_z-1)
        ]
    while q:
        d = q.pop()
        # print(d)
        if d in exterior_droplets:
            # print('in ed')
            continue
        if d in droplets:
            # print('in d')
            continue
        exterior_droplets.add(d)
        for n in generate_neighbors(d):
            if ((min_x-1 <= n.x <= max_x+1) and \
                (min_y-1 <= n.y <= max_y+1) and \
                (min_z-1 <= n.z <= max_z+1)) and \
                n not in droplets:
               q.append(n)


    return exterior_droplets

"""
Something seems off about your calculation. The cooling rate depends on exterior surface area, but your calculation also included the surface area of air pockets trapped in the lava droplet.

Instead, consider only cube sides that could be reached by the water and steam as the lava droplet tumbles into the pond. The steam will expand to reach as much as possible, completely displacing any air on the outside of the lava droplet but never expanding diagonally.

In the larger example above, exactly one cube of air is trapped within the lava droplet (at 2,2,5), so the exterior surface area of the lava droplet is 58.
"""
def part2(file_name):
    droplets = set(read_droplets(file_name))

    exterior_spots = find_exterior_droplets(droplets)

    # print(f"drops:{len(droplets)}; exdrops:{len(exterior_spots)}")
    # print(droplets)
    # print(exterior_spots)

    exposed_faces = 0
    for d in droplets:
        ef = 0
        for n in generate_neighbors(d):
            if n in exterior_spots:
                ef += 1
        exposed_faces += ef


    return exposed_faces

print("part 1")
# 64
print(part1('example.txt'))
# 3564
print(part1('input.txt'))

print("part 2")
# 58
print(part2('example.txt'))
# 2106
print(part2('input.txt'))