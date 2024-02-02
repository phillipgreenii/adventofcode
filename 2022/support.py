import os
from typing import Generator

class Input:
    def __init__(self, lines):
        self._lines = lines

    def lines(self, skip_blanks=False)->Generator[str,None,None]:
        for l in self._lines:
            if skip_blanks and len(l) == 0:
                continue
            yield l
    
    def slurp(self):
        return "\n".join(self._lines)


def _find_day_path(day):
    root = os.path.dirname(os.path.abspath(__file__))
    d = os.path.join(root, day)
    if not os.path.exists(d):
        raise ValueError("unknown day: " + day)
    return d

def _find_input(day,part):
    d = _find_day_path(day)
    filename = os.path.join(d, part + "-input.private.txt")
    if os.path.exists(filename):
        return filename
    filename = os.path.join(d, "input.private.txt")
    if os.path.exists(filename):
        return filename
    raise ValueError("unknown part: " + part)

def load_input(day,part)->Input:
    filename = _find_input(day,part)

    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return Input(lines)


def _find_example(day,example):
    d = _find_day_path(day)

    filename = os.path.join(d, example + ".private.txt")
    if os.path.exists(filename):
        return filename

    raise ValueError("unknown example: " + example)

def load_file(day,day_filename_wo_ext)->Input:
    filename = _find_example(day,day_filename_wo_ext)

    with open(filename) as file:
        lines = [line.rstrip() for line in file]
    return Input(lines)

def load_example(day,example)->Input:
    return load_file(day,example)