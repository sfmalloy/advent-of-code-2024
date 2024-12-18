from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import deque, defaultdict


@advent.parser(18)
def parse(file: TextIOWrapper):
    B = []
    for line in file.readlines():
        c, r = map(int, line.split(','))
        B.append(Vec2(r, c))
    return B


@advent.solver(18, part=1)
def solve1(B: list[Vec2]):
    B = B[:1024]
    R = C = 71
    grid = [[0 for _ in range(C)] for _ in range(R)]
    for b in B:
        grid[b.r][b.c] = 1
    
    q = deque([(Vec2(0, 0), 0)])
    end = Vec2(R-1, C-1)
    visited = set()
    while q:
        pos, L = q.popleft()
        if pos == end:
            return L
        if pos in visited:
            continue
        visited.add(pos)
        for d in RCDir.all:
            new = pos + d
            if new.in_bounds_rc(grid) and not grid[new.r][new.c] and new not in visited:
                q.append((new, L+1))


@advent.solver(18, part=2)
def solve2(B: list[Vec2]):
    R = C = 71
    LIMIT = 1024
    grid = [[0 for _ in range(C)] for _ in range(R)]
    for b in B[:LIMIT]:
        grid[b.r][b.c] = 1
    
    i = LIMIT
    prev_path = find_path(grid)
    cutoff = B[i]
    while prev_path:
        cutoff = B[i]
        grid[cutoff.r][cutoff.c] = 1
        if cutoff in prev_path:
            prev_path = find_path(grid)
        i += 1
    return f'{cutoff.c},{cutoff.r}'


def find_path(grid: list[list[int]]):
    R = C = len(grid)
    q = deque([(Vec2(0, 0), set())])
    end = Vec2(R-1, C-1)
    visited = set()
    while q:
        pos, path = q.popleft()
        if pos == end:
            return path
        if pos in visited:
            continue
        visited.add(pos)
        for d in RCDir.all:
            new = pos + d
            if new.in_bounds_rc(grid) and not grid[new.r][new.c] and new not in visited:
                q.append((new, path | {pos}))
    return None
