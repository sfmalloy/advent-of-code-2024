from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import deque, defaultdict


@advent.parser(10)
def parse(file: TextIOWrapper):
    return [[int(t) for t in line.strip()] for line in file.readlines()]


@advent.solver(10)
def solve(trail: list[list[int]]) -> int:
    q: deque[tuple[int, Vec2]] = deque()
    for r, row in enumerate(trail):
        for c, col in enumerate(row):
            if col == 0:
                q.append((len(q), Vec2(r, c)))
    
    visited = defaultdict(set)
    part1 = defaultdict(set)
    part2 = 0
    while q:
        id, pos = q.popleft()
        visited[id].add(pos)
        if trail[pos.r][pos.c] == 9:
            part1[id].add(pos)
            part2 += 1
            continue
        for dir in RCDir.all:
            new = pos + dir
            if (
                new.in_bounds_rc(trail) 
                and new not in visited[id] 
                and trail[new.r][new.c] - trail[pos.r][pos.c] == 1
            ):
                q.append((id, new))
    return sum(len(e) for e in part1.values()), part2
