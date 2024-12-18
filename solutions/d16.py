from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import defaultdict
from queue import PriorityQueue


@advent.parser(16)
def parse(file: TextIOWrapper):
    grid = [line.strip() for line in file.readlines()]
    return grid, Vec2(len(grid)-2, 1), Vec2(1, len(grid[1])-2)


@advent.solver(16)
def solve(grid: list[list[str]], start: Vec2, end: Vec2):
    q: PriorityQueue[tuple[int, Vec2, Vec2, set]] = PriorityQueue()
    q.put((0, start, RCDir.E, set()))
    dist = defaultdict(lambda: float('inf'))
    dist[start] = 0
    visited = set()
    sit = set()
    while not q.empty():
        cost, pos, dir, path = q.get()
        if pos == end:
            if cost == dist[end]:
                sit |= path 
            continue
        visited.add((pos, dir))
        for d in RCDir.all:
            new = pos + d
            move_cost = 1001 if d != dir else 1
            if grid[new.r][new.c] != '#' and (new, d) not in visited:
                q.put((cost + move_cost, new, d, path | {pos}))
                if cost + move_cost < dist[new]:
                    dist[new] = cost + move_cost
    return dist[end], len(sit) + 1
