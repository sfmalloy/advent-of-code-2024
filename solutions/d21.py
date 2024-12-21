from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import deque
from functools import cache

NUMERIC_KEYPAD = [
    '789',
    '456',
    '123',
    '.0A'
]

DIRECTIONAL_KEYPAD = [
    '.^A',
    '<v>'
]

MOVE_SYMBOLS = {
    RCDir.U: '^',
    RCDir.D: 'v',
    RCDir.L: '<',
    RCDir.R: '>'
}


@advent.parser(21)
def parse(file: TextIOWrapper):
    return [line.strip() for line in file.readlines()]


@advent.solver(21, part=1)
def solve1(codes: list[str]):
    return sum(code_length(code, 2) for code in codes)


@advent.solver(21, part=2)
def solve2(codes: list[str]):
    return sum(code_length(code, 25) for code in codes)


def code_length(code: str, robot_dpads: int):
    return int(code[:-1]) * find_path(code, robot_dpads + 1)


@cache
def find_path(goal_seq: str, num_robots: int, dimension: int=0):
    if dimension == num_robots:
        return len(goal_seq)

    src = 'A'
    L = 0
    for dst in goal_seq:
        best = float('inf')
        for path in shortest_paths(src, dst, dimension == 0):
            path += 'A'
            best = min(best, find_path(path, num_robots, dimension + 1))
        L += best
        src = dst
    return L


@cache
def shortest_paths(src: str, dst: str, use_numeric: bool):
    keypad = NUMERIC_KEYPAD if use_numeric else DIRECTIONAL_KEYPAD
    q = deque([(find_symbol(keypad, src), '')])
    paths = []
    shortest_len = float('inf')
    while q:
        pos, path = q.popleft()
        if len(path) > shortest_len:
            continue
        if keypad[pos.r][pos.c] == dst:
            shortest_len = min(shortest_len, len(path))
            paths.append(path)
            continue
        for d in RCDir.all:
            new = pos + d
            if new.in_bounds_rc(keypad) and keypad[new.r][new.c] != '.':
                q.append((new, path + MOVE_SYMBOLS[d]))
    return paths


def find_symbol(keypad: list[str], symbol: str) -> Vec2 | None:
    for r, row in enumerate(keypad):
        if (c := row.find(symbol)) != -1:
            return Vec2(r, c)
    return None
