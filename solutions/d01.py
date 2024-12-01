from io import TextIOWrapper
from lib.advent import advent

@advent.parser(1)
def parse(file: TextIOWrapper):
    a = []
    b = []
    for line in file.readlines():
        x, y = map(int, line.split())
        a.append(x)
        b.append(y)
    return sorted(a), sorted(b)


@advent.solver(1, part=1)
def solve1(a: list[int], b: list[int]) -> int:
    t = 0
    for x, y in zip(a, b):
        t += abs(y-x)
    return t


@advent.solver(1, part=2)
def solve2(a: list[int], b: list[int]) -> int:
    t = 0
    for x in a:
        t += x * b.count(x)
    return t
