from support import Input

def to_me(them):
    return chr(ord(them) - ord('A') + ord('X'))

def to_them(me):
    return chr(ord(me) - ord('X') + ord('A'))

def score_guess(me):
    if me == 'X':
        shape_score = 1
    elif me == 'Y':
        shape_score = 2
    elif me == 'Z':
        shape_score = 3
    return shape_score

def score_round(them, me):
    me = to_them(me)
    if them == me:
        round_score = 3
    elif them == 'A' and me == 'C':
        round_score = 0
    elif them == 'C' and me == 'A':
        round_score = 6
    elif them == 'B' and me == 'C':
        round_score = 6
    elif them == 'C' and me == 'B':
        round_score = 0
    elif them == 'B' and me == 'A':
        round_score = 0
    elif them == 'A' and me == 'B':
        round_score = 6
    return round_score

def part1(input:Input)->str:
    total_score = 0
    for line in input.lines():
        (them, me) = line.split()
        total_score += score_guess(me) + score_round(them, me)
    
    return str(total_score)

def calc_guess(them, result):
    if result == 'Y':
        return to_me(them)
    elif result == 'X' and them == 'A':
        return to_me('C')
    elif result == 'X' and them == 'B':
        return to_me('A')
    elif result == 'X' and them == 'C':
        return to_me('B')
    elif result == 'Z' and them == 'A':
        return to_me('B')
    elif result == 'Z' and them == 'B':
        return to_me('C')
    elif result == 'Z' and them == 'C':
        return to_me('A')

def part2(input:Input)->str:
    total_score = 0
    for line in input.lines():
        (them, result) = line.split()
        me = calc_guess(them, result)
        total_score += score_guess(me) + score_round(them, me)
    
    return str(total_score)
