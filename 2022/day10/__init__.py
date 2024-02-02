from support import Input


def read_operations(operations, input:Input):
    op_lookup = {operation.opcode: operation for operation in operations}

    for line in input.lines(skip_blanks=True):
        opcode, *args = line.split()
        op = op_lookup[opcode]
        params = op.parse_params(args)
        yield (op, params)

class Operation:

    def __init__(self, opcode, duration, parse_params, action):
        self.opcode = opcode
        self.duration = duration
        self.parse_params = parse_params
        self.action = action

    def __repr__(self):
        return f"{self.opcode}"

    def run(self, registers, params):
        # print(f"{self.opcode}: 0")
        for x in range(self.duration-1):
            # print(f"{self.opcode}: 1")
            yield
        # print(f"{self.opcode}: 2")
        self.action(registers, params)
        yield
        # print(f"{self.opcode}: 3")

def generate_operations():
    def noop(registers, params):
        pass
    def noop_parse_params(args):
        return ()
    op_noop = Operation('noop', 1, noop_parse_params, noop)

    def addx(registers, params):
        registers['x'] += params[0]
    def addx_parse_params(args):
        return (int(args[0]), )
    op_addx = Operation('addx', 2, addx_parse_params, addx)

    return [op_noop, op_addx]

def generate_signal(input:Input):
    registers = dict({'x':1})
    yield registers['x'], ''
    for operation, params in read_operations(generate_operations(), input):
        # print(f"Running {operation}: {params}")
        for _ in operation.run(registers, params):
            # print(f"Tick {operation} ({registers['x']})")
            yield registers['x'], operation.opcode
        # print(f"Finish {operation}: {params}")

def print_signal(signal):
    signal = list(signal)
    print(f"signal of size: ({len(signal)})")
    for cycle, val in enumerate(signal):
        print(f"{cycle:3} {val[1]:5} :{val[0]:4}")
    print()

def part1(input:Input)->str:

    signal = list(generate_signal(input))
    # print_signal(signal)

    cycles_to_check = [20, 60, 100, 140, 180, 220]

    signal_strengths = []
    for cycle in cycles_to_check:
        # subtract one because the signal is indexed such that 
        # pos x shows the result after step x, not during
        index = cycle - 1
        # print(f"{cycle}*{signal[index][0]}={signal[index][0] * cycle}")
        signal_strengths.append(signal[index][0] * cycle)


    return str(sum(signal_strengths))

def chunk_signal(signal, size):
    return [ signal[i:i+size] for i in range(0, len(signal), size) ]

def render_signal_to_crt(signal, width=40, height=6):
    crt = [[' '] *width for i in range(height)]

    # this is a bit of a hack; it seems that this code uses the position of 
    # the signal to mark the value at the end of the cycle, but the problem 
    # refers to it during the cycle.  It seems in practices this results in 
    # an off by one. Therefor, the remaining item gets lopped off
    trimmed_signal = signal[:(width*height)]
    for y, chunk in enumerate(chunk_signal(trimmed_signal, width)):
        for x,s in enumerate(chunk):
            if s-1 <= x <= s+1:
                crt[y][x] = '#'
            else:
                crt[y][x] = '.'
        

    return '\n'.join([ ''.join(r) for r in crt ])

def part2(input:Input)->str:

    signal = list(map(lambda x: x[0],generate_signal(input)))
    # print(signal)
    
    return render_signal_to_crt(signal)
