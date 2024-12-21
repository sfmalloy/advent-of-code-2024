from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import deque


g_cache = {}

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


@advent.parser(21)
def parse(file: TextIOWrapper):
    return [line.strip() for line in file.readlines()]


@advent.solver(21, part=1)
def solve1(codes: list[str]):
    global g_cache
    g_cache = {}
    ans = 0
    for code in codes:
        ans += int(code[:-1]) * find_path(code, 3, 0)
    return ans


@advent.solver(21, part=2)
def solve2(codes: list[str]):
    global g_cache
    g_cache = {}
    ans = 0
    for code in codes:
        ans += int(code[:-1]) * find_path(code, 26, 0)
    return ans


def find_path(goal_seq: str, num_keypads: int, dimension: int=0):
    if (goal_seq, dimension) in g_cache:
        return g_cache[(goal_seq, dimension)]
    if dimension == num_keypads:
        return len(goal_seq)

    keypad = NUMERIC_KEYPAD if dimension == 0 else DIRECTIONAL_KEYPAD
    src = 'A'
    L = 0
    for dst in goal_seq:
        best = float('inf')
        for path in shortest_paths(src, dst, keypad):
            path += 'A'
            best = min(best, find_path(path, num_keypads, dimension + 1))
        L += best
        src = dst
    g_cache[(goal_seq, dimension)] = L
    return L


def shortest_paths(src: str, dst: str, keypad: list[str]):
    move_symbols = {
        RCDir.U: '^',
        RCDir.D: 'v',
        RCDir.L: '<',
        RCDir.R: '>'
    }
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
                q.append((new, path + move_symbols[d]))
    return paths


def find_symbol(keypad: list[str], symbol: str) -> Vec2 | None:
    for r, row in enumerate(keypad):
        if (c := row.find(symbol)) != -1:
            return Vec2(r, c)
    return None
