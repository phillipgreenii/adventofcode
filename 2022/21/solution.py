def read_lines(file_name, skip_blanks=True):
    with open(file_name) as file_in:
        for line in file_in:
            line = line.rstrip()
            if skip_blanks and line == '':
                continue
            yield line

from enum import Enum
from typing import NamedTuple, List, Iterator, Set, Dict, Optional, Tuple, Union

class ValueMonkey(NamedTuple):
    value:int

class OperationMonkey(NamedTuple):
    operation:str
    param1:str
    param2:str

def parse_monkey(line:str)->Tuple[str,Union[ValueMonkey,OperationMonkey]]:
    parts = line.split(':')
    name = parts[0]
    parts = parts[1].split()
    if len(parts) == 1:
        return (name, ValueMonkey(int(parts[0])))
    else: 
        return (name, OperationMonkey(parts[1],parts[0],parts[2]))
    

def read_monkeys(file_name:str)->Dict[str,Union[ValueMonkey,OperationMonkey]]:
    return { name:monkey for name,monkey in map(parse_monkey,read_lines(file_name)) }


def determine_value(monkeys,monkey_name) -> int:
    v = monkeys[monkey_name]
    if isinstance(v,ValueMonkey):
        return v.value
    else:
        if v.operation == '+':
            return determine_value(monkeys,v.param1) + determine_value(monkeys,v.param2)
        elif v.operation == '-':
            return determine_value(monkeys,v.param1) - determine_value(monkeys,v.param2)
        elif v.operation == '*':
            return determine_value(monkeys,v.param1) * determine_value(monkeys,v.param2)
        elif v.operation == '/':
            return determine_value(monkeys,v.param1) // determine_value(monkeys,v.param2)
        else: 
            raise Exception(f"Unknown operation: {v}")


def part1(file_name):
    monkeys = read_monkeys(file_name)
    print(monkeys)
    # print(determine_value(monkeys,'dbpl'))

    result = determine_value(monkeys, 'root')
    return result

    
"""
Due to some kind of monkey-elephant-human mistranslation, you seem to have misunderstood a few key details about the riddle.

First, you got the wrong job for the monkey named root; specifically, you got the wrong math operation. The correct operation for monkey root should be =, which means that it still listens for two numbers (from the same two monkeys as before), but now checks that the two numbers match.

Second, you got the wrong monkey for the job starting with humn:. It isn't a monkey - it's you. Actually, you got the job wrong, too: you need to figure out what number you need to yell so that root's equality check passes. (The number that appears after humn: in your input is now irrelevant.)

In the above example, the number you need to yell to pass root's equality test is 301. (This causes root to get the same number, 150, from both of its monkeys.)

What number do you yell to pass root's equality test?
"""
def part2(file_name):
    pass

print("part 1")
# 15
print(part1('example.txt'))
# 3068
print(part1('input.txt'))

print("part 2")
# 301
print(part2('example.txt'))
# ?
# print(part2('input.txt'))