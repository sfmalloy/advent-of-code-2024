import math
from lib import advent
from io import TextIOWrapper
from functools import lru_cache


@advent.parser(11)
def parse(file: TextIOWrapper):
    return list(map(int, file.read().strip().split()))


@advent.solver(11, part=1)
def solve1(ipt):
    t = 0
    for i in ipt:
        t += transform(i, 25)
    return t


@advent.solver(11, part=2)
def solve2(ipt):
    t = 0
    for i in ipt:
        t += transform(i, 75)
    return t


@lru_cache(maxsize=None)
def transform(num: int, iters: int):
    if iters == 0:
        return 1
    if num == 0:
        return transform(1, iters-1)

    mag = magnitude(num)
    if mag % 2 == 0:
        mag //= 2
        m = 10**mag
        return transform(num // m, iters-1) + transform(num % m, iters-1)
    return transform(num * 2024, iters-1)


def magnitude(a: int):
    return int(math.log10(a) + 1)

