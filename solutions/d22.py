from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict


@advent.parser(22)
def parse(file: TextIOWrapper):
    return [int(line.strip()) for line in file.readlines()]


@advent.solver(22)
def solve(nums: list[int]) -> tuple[int, int]:
    bananas = defaultdict(int)
    added = []
    p1 = 0
    for i, secret in enumerate(nums):
        added.append(set())
        prev = secret % 10
        diffs_row = deque()
        for _ in range(2000):
            secret = transform(secret)
            diffs_row.append((secret % 10) - prev)
            prev = secret % 10
            if len(diffs_row) < 4:
                continue
            if (diffs := tuple(diffs_row)) not in added[i]:
                added[i].add(diffs)
                bananas[diffs] += prev
            diffs_row.popleft()
        p1 += secret
    return p1, max(bananas.values())


def transform(secret: int) -> int:
    secret = (secret ^ (secret << 6)) % 16777216
    secret = (secret ^ (secret >> 5)) % 16777216
    return (secret ^ (secret << 11)) % 16777216
