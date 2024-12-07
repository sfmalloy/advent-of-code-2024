from lib import advent
from io import TextIOWrapper
from math import log10


@advent.parser(7)
def parse(file: TextIOWrapper):
    equations = {}
    for line in file.readlines():
        key, vals = line.split(': ')
        equations[int(key)] = list(map(int, vals.split()))
    return equations


@advent.solver(7)
def solve(equations: dict[int, list[int]]):
    p1 = 0
    p2 = 0
    for ans, vals in equations.items():
        if find_ops_no_concat(ans, vals):
            p1 += ans
            p2 += ans
        elif find_ops_concat(ans, vals):
            p2 += ans
    return p1, p2


def find_ops_no_concat(ans: int, vals: list[int]):
    if not vals:
        return ans == 0
    valslice = vals[:-1]
    test = False

    if ans % vals[-1] == 0:
        test = test or find_ops_no_concat(ans // vals[-1], valslice)
    
    if not test and ans - vals[-1] >= 0:
        test = test or find_ops_no_concat(ans - vals[-1], valslice)

    return test

def find_ops_concat(ans: int, vals: list[int]):
    if not vals:
        return ans == 0

    valslice = vals[:-1]
    test = False

    if ans % vals[-1] == 0:
        test = test or find_ops_concat(ans // vals[-1], valslice)
    
    if not test and ans - vals[-1] >= 0:
        test = test or find_ops_concat(ans - vals[-1], valslice)
    
    mag = 10**magnitude(vals[-1])
    if not test and ans % mag == vals[-1]:
        test = test or find_ops_concat(ans // mag, valslice)
    
    return test


def magnitude(a: int):
    return int(log10(a) + 1)
