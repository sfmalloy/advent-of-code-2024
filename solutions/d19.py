from lib import advent
from io import TextIOWrapper
from collections import defaultdict


@advent.parser(19)
def parse(file: TextIOWrapper):
    groups = file.read().split('\n\n')
    patterns = defaultdict(set)
    for pattern in groups[0].strip().split(', '):
        patterns[len(pattern)].add(pattern)
    return patterns, groups[1].splitlines()


@advent.solver(19)
def solve1(patterns: defaultdict[int, set], towels: list[str]):
    global cache
    cache = {}

    p1 = 0
    p2 = 0
    for towel in towels:
        if (count := count_possible(patterns, towel)) > 0:
            p1 += 1
            p2 += count
    return p1, p2


def count_possible(patterns: defaultdict[int, set], towel: str, ptr: int = 0):
    if (towel, ptr) in cache:
        return cache[(towel, ptr)]
    if ptr == len(towel):
        return 1
    count = 0
    for length in range(min(patterns), max(patterns)+1):
        sub = towel[ptr:ptr+length]
        if sub in patterns[length]:
            count += count_possible(patterns, towel, ptr + length)
    cache[(towel, ptr)] = count
    return cache[(towel, ptr)]
