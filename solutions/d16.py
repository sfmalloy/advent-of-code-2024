from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import defaultdict
from heapq import heappush, heappop


@advent.parser(16)
def parse(file: TextIOWrapper):
    grid = [line.strip() for line in file.readlines()]
    return grid, Vec2(len(grid)-2, 1), Vec2(1, len(grid[1])-2)


@advent.solver(16)
def solve(grid: list[list[str]], start: Vec2, end: Vec2) -> tuple[int, int]:
    q: list[tuple[int, Vec2, Vec2, set]] = []
    heappush(q, (0, start, RCDir.E, set()))
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    visited = set()
    sit = set()
    while q:
        cost, pos, dir, path = heappop(q)
        if pos == end:
            if cost == dist[end]:
                sit |= path 
            continue
        visited.add((pos, dir))
        for d in RCDir.all:
            new = pos + d
            move_cost = 1001 if d != dir else 1
            if grid[new.r][new.c] != '#' and (new, d) not in visited:
                heappush(q, (cost + move_cost, new, d, path | {pos}))
                if cost + move_cost < dist[new]:
                    dist[new] = cost + move_cost
    return dist[end], len(sit) + 1
