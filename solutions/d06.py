from lib import advent
from io import TextIOWrapper
from lib.common.vec import Vec2, RCDir


@advent.parser(6)
def parse(file: TextIOWrapper):
    grid = []
    pos = Vec2(0, 0)
    for r, line in enumerate(file.readlines()):
        row = []
        for c, col in enumerate(line.strip()):
            if col == '^':
                row.append('.')
                pos = Vec2(r, c)
            else:
                row.append(col)
        grid.append(row)
    return grid, pos


DELTAS = [RCDir.U, RCDir.R, RCDir.D, RCDir.L]

@advent.solver(6, part=1)
def solve1(grid: list[str], pos: Vec2):
    visited = set()
    curdir = 0
    in_bounds = True
    while in_bounds:
        visited.add(pos)
        pos += DELTAS[curdir]
        in_bounds = pos.in_bounds_rc(grid)
        if in_bounds and grid[pos.r][pos.c] == '#':
            pos -= DELTAS[curdir]
            curdir = (curdir + 1) % 4
    return len(visited)


@advent.solver(6, part=2)
def solve2(grid: list[str], pos: Vec2):
    dir = 0
    path: list[tuple[Vec2, int]] = []
    firsts = {}
    in_bounds = True
    prev = pos
    while in_bounds:
        path.append((pos, dir))
        if pos not in firsts:
            firsts[pos] = (prev, dir, len(path)-1)
        pos += DELTAS[dir]
        in_bounds = pos.in_bounds_rc(grid)
        if in_bounds and grid[pos.r][pos.c] == '#':
            pos -= DELTAS[dir]
            dir = (dir + 1) % 4
        prev = pos
    
    new = set()
    for curr, _ in path[1:]:
        if grid[curr.r][curr.c] == '.':
            grid[curr.r][curr.c] = '#'
            if curr not in new and find_loop(grid, firsts[curr][0], firsts[curr][1], set(path[:firsts[curr][2]])):
                new.add(curr)
            grid[curr.r][curr.c] = '.'
    return len(new)


def find_loop(grid: list[str], pos: Vec2, curdir: int, visited: set):
    in_bounds = True
    while in_bounds:
        if (pos, curdir) in visited:
            return True
        in_bounds = pos.in_bounds_rc(grid)
        if in_bounds and grid[pos.r][pos.c] == '#':
            pos -= DELTAS[curdir]
            curdir = (curdir + 1) % 4
        visited.add((pos, curdir))
        pos += DELTAS[curdir]
    return False
