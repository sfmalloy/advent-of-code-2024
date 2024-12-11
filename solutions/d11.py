from lib import advent
from lib.common import magnitude
from io import TextIOWrapper
from functools import lru_cache


@advent.parser(11)
def parse(file: TextIOWrapper) -> list[int]:
    return list(map(int, file.read().strip().split()))


@advent.solver(11, part=1)
def solve1(stones: list[int]) -> int:
    return sum(blink(s, 25) for s in stones)


@advent.solver(11, part=2, reparse=False)
def solve2(stones: list[int]) -> int:
    return sum(blink(s, 75) for s in stones)


@lru_cache(maxsize=None)
def blink(num: int, B: int):
    if B == 0:
        return 1
    if num == 0:
        return blink(1, B-1)

    mag = magnitude(num)
    if mag % 2 == 0:
        m = 10**(mag//2)
        return blink(num // m, B-1) + blink(num % m, B-1)
    return blink(num * 2024, B-1)

