from lib import advent
from io import TextIOWrapper
from lib.common.parsers import intlist
from itertools import pairwise, compress


@advent.parser(2)
def parse(file: TextIOWrapper) -> list[int]:
    return [intlist(line.strip()) for line in file.readlines()]


@advent.solver(2, part=1)
def solve1(reports: list[list[int]]) -> int:
    return sum(find_reports(reports, True))


@advent.solver(2, part=2, reparse=False, use_part1=True)
def solve2(reports: list[list[int]], part1: int):
    return part1 + sum(
        (any(test(unsafe[:i] + unsafe[i+1:], True) for i in range(len(unsafe)))) 
        for unsafe in compress(reports, find_reports(reports, False))
    )


def find_reports(reports: list[list[int]], safe: bool):
    return [test(levels, safe) for levels in reports]


def test(levels: list[int], safe: bool):
    # I just wanted to do this in one line and use an itertool I never use
    # ...it's not that efficient
    return (
        (not any(
            abs(a - b) < 1 or abs(a - b) > 3
            for a, b in pairwise(levels)
        ) and (
            all(a - b > 0 for a, b in pairwise(levels))
            or all(a - b < 0 for a, b in pairwise(levels))
        )) ^ (not safe)
    )
