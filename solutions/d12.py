from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
from lib.common.vec import Vec2, RCDir

@advent.parser(12)
def parse(file: TextIOWrapper):
    return [list(line.strip()) for line in file.readlines()]


@advent.solver(12, part=1)
def solve1(garden: list[list[str]]):
    price = 0
    for r, row in enumerate(garden):
        for c, col in enumerate(row):
            if col.isupper():
                price += calculate_price(garden, col, Vec2(r, c))
    return price


@advent.solver(12, part=2)
def solve2(garden: list[list[str]]):
    price = 0
    for r, row in enumerate(garden):
        for c, col in enumerate(row):
            if col.isupper():
                price += mark_fence(garden, col, Vec2(r, c))
    return price


def calculate_price(garden: list[list[str]], symbol: str, pos: Vec2):
    perim = 0
    area = 0
    q = deque([pos])
    while q:
        front = q.pop()
        if garden[front.r][front.c] == symbol.lower():
            continue
        garden[front.r][front.c] = symbol.lower()
        area += 1
        for dir in RCDir.all:
            neighbor = front + dir
            if not neighbor.in_bounds_rc(garden) or garden[neighbor.r][neighbor.c].lower() != symbol.lower():
                perim += 1
            elif garden[neighbor.r][neighbor.c] == symbol:
                q.append(neighbor)
    return perim * area


def mark_fence(garden: list[list[str]], symbol: str, pos: Vec2):
    plot_points: set[Vec2] = set()
    area = 0
    q = deque([pos])
    while q:
        front = q.pop()
        plot_points.add(front)
        if garden[front.r][front.c] == symbol.lower():
            continue
        garden[front.r][front.c] = symbol.lower()
        area += 1
        for dir in RCDir.all:
            neighbor = front + dir
            if neighbor.in_bounds_rc(garden) and garden[neighbor.r][neighbor.c] == symbol:
                q.append(neighbor)
    
    plot = []    
    for r in range(min(v.r for v in plot_points), max(v.r for v in plot_points)+1):
        row = []
        for c in range(min(v.c for v in plot_points), max(v.c for v in plot_points)+1):
            if Vec2(r, c) in plot_points:
                row.append(symbol)
            else:
                row.append('.')
        plot.append(row)

    plot = add_vertical_padding(plot, symbol)
    plot = add_vertical_padding(list(map(list, zip(*plot))), symbol)

    fences: set[Vec2] = set()
    for r, row in enumerate(plot):
        for c, col in enumerate(row):
            if col == '#':
                fences.add(Vec2(r, c))
            elif col == symbol:
                plot[r][c] = '.'

    sides = 0
    while fences:
        curr = min(fences)
        dir = RCDir.R
        sides += 1
        for _ in range(4):
            if (curr+dir).in_bounds_rc(plot) and (curr+dir) in fences:
                break
            dir = RCDir.clockwise(dir)
        while curr in fences:
            plot[curr.r][curr.c] = '.'
            fences.remove(curr)
            curr += dir
    return area * sides


def add_vertical_padding(plot: list[list[str]], symbol: str):
    new_plot = []
    for r, row in enumerate(plot):
        # top
        v_pad = []
        for c, col in enumerate(plot[r]):
            if col == symbol:
                neighbor = Vec2(r-1, c)
                if not neighbor.in_bounds_rc(plot) or plot[neighbor.r][neighbor.c] == '.':
                    v_pad.append('#')
                else:
                    v_pad.append(col)
            else:
                v_pad.append(col)
        new_plot.append(v_pad)
        new_plot.append([c for c in row])

        # bottom
        v_pad = []
        for c, col in enumerate(plot[r]):
            if col == symbol:
                neighbor = Vec2(r+1, c)
                if not neighbor.in_bounds_rc(plot) or plot[neighbor.r][neighbor.c] == '.':
                    v_pad.append('#')
                else:
                    v_pad.append(col)
            else:
                v_pad.append(col)
        new_plot.append(v_pad)
    return new_plot
