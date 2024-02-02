from support import Input


class Monkey:
    def __init__(self):
        self.items = []
        self.inspections = 0
        self.op = None
        self.test = None
        self.test_val = None
        self.monkey_when_true = None
        self.monkey_when_false = None
    
    def __repr__(self):
        items = ",".join(map(str,self.items))
        return f"Monkey({self.inspections}:{items})"

def read_items(line):
    parts = line.split(':')
    items = parts[1].split(',')
    return list(map(int,items))

def read_op(line):
    parts = line.split()
    # print(parts)
    param1 = parts[-3]
    operator = parts[-2]
    param2 = parts[-1]
    if param1 == 'old':
        param1 = lambda i: i
    else:
        x1 = int(param1)
        param1 = lambda i: x1
    if operator == '+':
        operator = lambda p1,p2: p1+p2
    elif operator == '*':
        operator = lambda p1,p2: p1*p2
    else:
        raise Exception(f"Unknown Op: {operator}")
    if param2 == 'old':
        param2 = lambda i: i
    else:
        x1 = int(param2)
        param2 = lambda i: x1
    return lambda i: operator(param1(i),param2(i))

def read_test(line):
    parts = line.split()
    mod = int(parts[-1])
    return mod,lambda i: i%mod == 0

def read_test_result(line):
    parts = line.split()
    return int(parts[-1])

def read_monkeys(input:Input):
    lines = input.lines(skip_blanks=True)
    monkeys = []
    while True:
        try:
            # check for next monkey
            next(lines)
            monkey = Monkey()
            monkey.items = read_items(next(lines))
            monkey.op =read_op(next(lines))
            monkey.test_val, monkey.test = read_test(next(lines))
            monkey.monkey_when_true = read_test_result(next(lines))
            monkey.monkey_when_false = read_test_result(next(lines))
            monkeys.append(monkey)
        except StopIteration:
            break
    return monkeys

def log(msg_generator):
    #print(msg)
    # print(msg_generator())
    pass

def inspect_and_throw(monkeys, monkey,  item, worry_reducer):
    monkey.inspections += 1
    log(lambda : f"  Monkey inspects an item with a worry level of {item}.")
    item = monkey.op(item)
    log(lambda : f"    Worry level updated to {item}")
    item = worry_reducer(item)
    log(lambda : f"    Monkey gets bored with item. Worry level is lowered to {item}")
    test_result = monkey.test(item)
    trs = 'divisible' if test_result else 'not divisible'
    log(lambda : f"    Current worry level is {trs} by {monkey.test_val}")
    target = monkey.monkey_when_true if test_result else monkey.monkey_when_false
    log(lambda : f"    Item with worry level {item} is thrown to monkey {target}.")
    monkeys[target].items.append(item)

def perform_turn(monkeys, monkey, worry_reducer):
    items = monkey.items
    monkey.items = []
    for item in items:
        inspect_and_throw(monkeys, monkey, item, worry_reducer)

def perform_round(monkeys, worry_reducer):
    for i,m in enumerate(monkeys):
        log(lambda : f"Monkey {i}")
        perform_turn(monkeys, m, worry_reducer)

def part1(input:Input)->str:
    monkeys = read_monkeys(input)
    # print(monkeys)

    for _ in range(20):
        perform_round(monkeys, lambda i: i // 3)

    sorted_monkeys = sorted(monkeys,key=lambda m: m.inspections,reverse=True)
    # print(sorted_monkeys)

    inpection_counts = list(map(lambda m: m.inspections,sorted_monkeys))
    return str(inpection_counts[0] * inpection_counts[1])

def part2(input:Input)->str:
    import sys
    sys.set_int_max_str_digits(5000)
    monkeys = read_monkeys(input)

    all_test_levels = list(map(lambda m: m.test_val, monkeys))
    # print(all_test_levels)
    import math
    all_test_levels_lcm = math.lcm(*all_test_levels)
    # print(monkeys)
    def worry_reducer(item):
        # mod on LCM removes largest portion of the numbers, but maintains the test checks
        return item % all_test_levels_lcm
    

    # for _ in range(10_000):
    for _ in range(10_000):
        perform_round(monkeys, worry_reducer)

    sorted_monkeys = sorted(monkeys,key=lambda m: m.inspections,reverse=True)
    # print(sorted_monkeys)

    inpection_counts = list(map(lambda m: m.inspections,sorted_monkeys))
    return str(inpection_counts[0] * inpection_counts[1])
