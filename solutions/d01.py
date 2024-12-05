from lib import advent

from io import TextIOWrapper
from collections import defaultdict


@advent.parser(1)
def parse(file: TextIOWrapper) -> tuple[list[int], list[int]]:
    left = []
    right = []
    for line in file.readlines():
        l, r = map(int, line.split())
        left.append(l)
        right.append(r)
    return sorted(left), sorted(right)


@advent.solver(1, part=1)
def solve1(left: list[int], right: list[int]) -> int:
    return sum(abs(l - r) for l, r in zip(left, right))


@advent.solver(1, part=2, reparse=False)
def solve2(left: list[int], right: list[int]) -> int:
    counts = defaultdict(int)
    for r in right:
        counts[r] += 1
    return sum(l * counts[l] for l in left)
