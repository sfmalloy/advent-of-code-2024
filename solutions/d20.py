from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import deque


@advent.parser(20)
def parse(file: TextIOWrapper):
    grid = [line.strip() for line in file.readlines()]
    start = None
    end = None
    for row, line in enumerate(grid):
        if (col := line.find('S')) != -1:
            start = Vec2(row, col)
        elif (col := line.find('E')) != -1:
            end = Vec2(row, col)
    grid = [list(line) for line in grid]
    return grid, start, end


@advent.solver(20, part=1)
def solve1(grid: list[list[str]], start: Vec2, end: Vec2) -> int:
    dist_to_end, path = setup_race(grid, start, end)
    return find_cheats(2, dist_to_end, path)


@advent.solver(20, part=2)
def solve2(grid: list[list[str]], start: Vec2, end: Vec2):
    dist_to_end, path = setup_race(grid, start, end)
    return find_cheats(20, dist_to_end, path)


def find_cheats(cheat_limit: int, dist_to_end: dict[Vec2, int], path: list[Vec2]) -> int:
    count = 0
    for i, src in enumerate(path):
        for dst in path[i+1:]:
            dist = dst.manhattan_distance(src)
            if dist <= cheat_limit and dist > 1 and dist_to_end[src] - dist - dist_to_end[dst] >= 100:
                count += 1
    return count


def setup_race(grid: list[list[str]], start: Vec2, end: Vec2) -> tuple[dict[Vec2, int], list[Vec2]]:
    dist_setup = {}

    q = deque([(start, list())])
    visited = set()
    init_path = None
    while q:
        pos, path = q.popleft()
        if pos == end:
            init_path = path
        if pos in visited:
            continue
        visited.add(pos)
        for d in RCDir.all:
            new = pos + d
            if new.in_bounds_rc(grid) and (grid[new.r][new.c] != '#') and new not in visited:
                q.append((new, path + [pos]))
                dist_setup[pos] = len(path)
    
    dist_to_end = {}
    for k, v in dist_setup.items():
        dist_to_end[k] = len(init_path) - v
    dist_to_end[end] = 0
    init_path.append(end)
    return dist_to_end, init_path
