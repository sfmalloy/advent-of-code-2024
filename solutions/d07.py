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


def find_ops_no_concat(ans: int, vals: list[int], test: int=0):
    if not vals:
        return test == ans
    elif test > ans:
        return False
    return (
        find_ops_no_concat(ans, vals[1:], test + vals[0])
        or find_ops_no_concat(ans, vals[1:], ((test if test else 1) * vals[0]))
    )


def find_ops_concat(ans: int, vals: list[int], test: int=0):
    if not vals:
        return test == ans
    elif test > ans:
        return False
    return (
        find_ops_concat(ans, vals[1:], test + vals[0])
        or find_ops_concat(ans, vals[1:], ((test if test else 1) * vals[0]))
        or find_ops_concat(ans, vals[1:], concat(test, vals[0]))
    )


def concat(a: int, b: int):
    return a * 10**(int(log10(b))+1) + b
