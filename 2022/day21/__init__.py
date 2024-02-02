from support import Input

from enum import Enum
from typing import NamedTuple, List, Iterator, Set, Dict, Optional, Tuple, Union

class ValueMonkey(NamedTuple):
    value:int

class OperationMonkey(NamedTuple):
    operation:str
    param1:str
    param2:str

Monkey = Union[ValueMonkey,OperationMonkey]

def parse_monkey(line:str)->Tuple[str,Monkey]:
    parts = line.split(':')
    name = parts[0]
    parts = parts[1].split()
    if len(parts) == 1:
        return (name, ValueMonkey(int(parts[0])))
    else: 
        return (name, OperationMonkey(parts[1],parts[0],parts[2]))
    

def read_monkeys(input:Input)->Dict[str,Monkey]:
    return { name:monkey for name,monkey in map(parse_monkey,input.lines(skip_blanks=True)) }


def part1(input:Input):
    monkeys = read_monkeys(input)
    tree = build_tree(monkeys, 'root')
    # print(tree)
    tree = reduce_tree(tree)
    # print(tree)
    return str(tree.value)

Node = Union["ValueNode","OperationNode", "UnknownValueNode"]

class ValueNode(NamedTuple):
    value:int

class OperationNode(NamedTuple):
    operation:str
    node1:Node
    node2:Node

class UnknownValueNode(NamedTuple):
    name:str

def monkey2node(monkeys:Dict[str,Monkey], name:str)->Node:
    if name not in monkeys:
        return UnknownValueNode(name)
    monkey = monkeys[name]
    if isinstance(monkey,ValueMonkey):
        return ValueNode(monkey.value)
    else:
        return OperationNode(monkey.operation,monkey2node(monkeys,monkey.param1),monkey2node(monkeys,monkey.param2))

def build_tree(monkeys:Dict[str,Monkey], root:str)->Node:
    return monkey2node(monkeys,root)
    
def reduce_tree(tree:Node)->Node:
    if isinstance(tree,ValueNode):
        return tree
    if isinstance(tree,UnknownValueNode):
        return tree

    n1 = reduce_tree(tree.node1)
    n2 = reduce_tree(tree.node2)
    
    # check for partial evalution
    if isinstance(n1,OperationNode) or isinstance(n2,OperationNode)\
        or isinstance(n1,UnknownValueNode) or isinstance(n2,UnknownValueNode):
        if n1 == tree.node1 and n2 == tree.node2:
            return tree
        else:
            return OperationNode(tree.operation, n1, n2)
    
    # full evaluation
    o = tree.operation
    v1 = n1.value
    v2 = n2.value
    if o == '+':
        v = v1 + v2
    elif o == '-':
        v = v1 - v2
    elif o == '*':
        v = v1 * v2
    elif o == '/':
        v = v1 // v2
    else: 
        raise Exception(f"Unknown operation: {o}")
    return ValueNode(v)

operator_opposite = {
    '+':'-',
    '-':'+',
    '*':'/',
    '/':'*'
}

# x + 3 = 7 => x = 7 - 3

# x / 3 = 7 => x = 7 * 3
# x * 3 = 7 => x = 7 / 3

# 3 - x = 7 => x = -(7 - 3)
# 3 - (2 * x) = 7 => - (2 * x) = 7 - 3

def unwrap_operation(unknown:Node, value:Node)->Tuple[Node,Node]:
    if isinstance(unknown,UnknownValueNode):
        return unknown,value
    inverse = operator_opposite[unknown.operation]
    if isinstance(unknown.node1,ValueNode):
        v=unknown.node1
        op=unknown.node2

        # '-' is not cumlative, so need to re-org equations
        # 4 - x = v
        # =>
        # x = 4 - v
        if unknown.operation == '-':
            return op,OperationNode('-',v,value)
        # NOTE: similar logic should exist for / as well, but since we are doing int math, 
        # 1/x would always be 0 so the problem won't do this
    else:
        v=unknown.node2
        op=unknown.node1
    # print(f"{unknown.operation}=>{operator_opposite[unknown.operation]}")
    new_v = OperationNode(inverse,value,v)
    # if negate_value:
    #     new_v = OperationNode('*',ValueNode(-1),new_v)
    return op,new_v

def solve_for_unknown(tree:Node)->Node:
    if tree.operation != '=':
        raise Exception(f"operation ({tree.operation}) must be '='")
    if isinstance(tree.node1,ValueNode):
        value = tree.node1
        unknown = tree.node2
    else:
        value = tree.node2
        unknown = tree.node1
    while not isinstance(unknown,UnknownValueNode):
        # print('solving')
        # print_tree(unknown)
        # print_tree(value)
        unknown, value = unwrap_operation(unknown, value)
    value = reduce_tree(value)
    return value

def node2str(node:Node)->str:
    if isinstance(node,ValueNode):
        return str(node.value)
    if isinstance(node,UnknownValueNode):
        return str(node.name)
    
    return f"({node2str(node.node1)}{node.operation}{node2str(node.node2)})"


def print_tree(tree:Node)->None:
    print(node2str(tree))

def part2(input:Input)->str:
    monkeys = read_monkeys(input)
    # update root operation
    monkeys['root'] = OperationMonkey('=',monkeys['root'].param1,monkeys['root'].param2)
    # remove value for humn
    del monkeys['humn']

    tree = build_tree(monkeys, 'root')
    # print("initial tree")
    # print(tree.node1)
    # print(tree.node2)
    tree = reduce_tree(tree)
    # print("reduced tree")
    # print_tree(tree.node1)
    # print_tree(tree.node2)
    tree = solve_for_unknown(tree)
    # print("solved tree")
    # print_tree(tree)
    return str(tree.value)
