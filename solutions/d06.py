from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
from lib.common.vec import Vec2, RCDir
from dataclasses import dataclass, field
from typing import Optional


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


@dataclass(frozen=True)
class Node:
    pos: Vec2
    dir: int
    wall: Optional[Vec2] = None


@advent.solver(6, part=2)
def solve2(grid: list[str], pos: Vec2):
    start_pos = pos
    curdir = 0
    nodes: set[Vec2] = set()
    in_bounds = True
    while in_bounds:
        nodes.add(pos)
        pos += DELTAS[curdir]
        in_bounds = pos.in_bounds_rc(grid)
        if in_bounds and grid[pos.r][pos.c] == '#':
            pos -= DELTAS[curdir]
            curdir = (curdir + 1) % 4
    
    pos = start_pos
    new = 0
    for v in nodes:
        if grid[v.r][v.c] == '.':
            grid[v.r][v.c] = '#'
            if find_loop(grid, pos):
                new += 1
            grid[v.r][v.c] = '.'
    return new


def find_loop(grid: list[str], pos: Vec2):
    curdir = 0
    visited = set()
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
