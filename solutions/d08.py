from lib import advent
from lib.common.vec import Vec2
from io import TextIOWrapper
from collections import defaultdict


@advent.parser(8)
def parse(file: TextIOWrapper):
    antennas = defaultdict(list)
    lines = file.readlines()
    R = len(lines)
    C = len(lines[0].strip())
    for r, row in enumerate(lines):
        for c, col in enumerate(row.strip()):
            if col != '.':
                antennas[col].append(Vec2(r, c))
    return antennas, R, C


@advent.solver(8, part=1)
def solve1(antennas: defaultdict[str, list[Vec2]], R: int, C: int):
    antinodes = set()
    for points in antennas.values():
        for src in points:
            for dst in points:
                if src != dst:
                    node = dst - (src - dst)
                    if node.in_bounds_rc(None, 0, 0, R, C):
                        antinodes.add(node)
    return len(antinodes)


@advent.solver(8, part=2)
def solve2(antennas: defaultdict[str, list[Vec2]], R: int, C: int):
    antinodes = set()
    for points in antennas.values():
        for src in points:
            for dst in points:
                if src != dst:
                    delta = (src - dst)
                    node = dst
                    while node.in_bounds_rc(None, 0, 0, R, C):
                        antinodes.add(node)
                        node -= delta
    return len(antinodes)
