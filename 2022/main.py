import sys
import re
import importlib

import support

usage="""
Usage: python main.py d#.p#
where day is 1-25 and part is either 1 or 2 
"""
def _failure(s,ec):
    print(s+usage, file=sys.stderr)
    sys.exit(ec)

def parse_args(args):
    if len(args) != 1:
        _failure("Invalid number of arguments",1)
        
    regex = r"d(\d{1,2})\.p([12])"
    cmd_match = re.search(regex, args[0])
    (d_str, p_str) = (cmd_match.group(1),cmd_match.group(2))

    d = int(d_str)
    if d < 1 or d > 25:
        _failure("Valid Days: 1-25",2)
    p = int(p_str)

    module=f"day{d:02}"
    function=f"part{p}"
    return (module, function)

def main(args):
    (module,part) = parse_args(args)
    day_module = importlib.import_module(module)

    input = support.load_input(module,part)
    result = getattr(day_module, part)(input)
    print(result)

if __name__ == '__main__':
    main(sys.argv[1:])