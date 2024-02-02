from support import Input

from enum import Enum
from typing import NamedTuple, List, Iterator, Set, Dict, Optional, Tuple, Union

SNAFU_BASE = 5

def snafu2dec(snafu:str)->int:
    val = 0
    mutliplier = 1
    for l in snafu[::-1]:
        if l == '2':
            val += 2 * mutliplier
        elif l == '1':
            val += mutliplier
        elif l == '0':
            pass
        elif l == '-':
            val -= mutliplier
        elif l == '=':
            val -= 2 * mutliplier
        else:
            raise Exception(f"Unknown char: {l}")
        mutliplier *= SNAFU_BASE
    return val

import math
def dec2snafu(dec:int)->str:
    chars = []
    # convert to based 5
    max_power = math.ceil(math.log(dec,SNAFU_BASE))
    m = int(math.pow(SNAFU_BASE, max_power))
    while m > 0:
        # print(m)
        v = dec // m
        chars.append(v)
        dec = dec % m
        m //= SNAFU_BASE
    # print(chars)
    # adjust for 0-4 to -2-2
    for i in range(len(chars)-1,0,-1):
        if chars[i] > 2:
            chars[i-1] += 1
            chars[i] -= SNAFU_BASE
    # print(chars)
    # convert symbols
    for i in range(len(chars)):
        if chars[i] >= 0:
            chars[i] = str(chars[i])
        elif chars[i] == -1:
            chars[i] = '-'
        elif chars[i] == -2:
            chars[i] = '='
        else:
            raise Exception(f"Unknown value: {chars[i]}")
    # print(chars)
    while chars[0] == '0':
        chars.pop(0)
    return "".join(chars)

def read_numbers(input:Input)->str:
    return list(input.lines(skip_blanks=True))

def part1(input:Input)->str:
    numbers = read_numbers(input)
    # print(numbers)
    total = 0
    for n in map(snafu2dec, numbers):
        # print(n)
        total+=n
    # print(total)
    
    return dec2snafu(total)
