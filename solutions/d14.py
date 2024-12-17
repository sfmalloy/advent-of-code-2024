import re
import operator
from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper
from collections import deque
from functools import reduce


@advent.parser(14)
def parse(file: TextIOWrapper):
    robots = []
    for line in file.readlines():
        pc, pr, vc, vr = map(int, re.findall(r'-?\d+', line))
        robots.append((Vec2(pr, pc), Vec2(vr, vc)))
    return robots


@advent.solver(14, part=1)
def solve1(robots: list[tuple[Vec2, Vec2]]):
    R = 103
    C = 101
    quads = {
        Vec2(1, 1): 0,
        Vec2(1, -1): 0,
        Vec2(-1, 1): 0,
        Vec2(-1, -1): 0
    }
    for robot in robots:
        p, v = robot
        p += v * 100
        p = Vec2((p.r % R), (p.c % C)) - Vec2(R//2, C//2)
        if p.r != 0 and p.c != 0:
            quads[Vec2(-1 if p.r < 0 else 1, -1 if p.c < 0 else 1)] += 1
    return reduce(operator.mul, quads.values())


@advent.solver(14, part=2)
def solve2(robots: list[tuple[Vec2, Vec2]]):
    R = 103
    C = 101
    t = 0
    while True:
        t += 1
        pos = set()
        for i in range(len(robots)):
            p, v = step(robots[i], R, C)
            pos.add(p)
            robots[i] = (p, v)
        visited = set()
        for p in pos:
            if p not in visited:
                new_visits = count_neighbors(p, pos)
                # 229 is the size of the tree
                if len(new_visits) == 229:
                    return t
                visited |= new_visits


def step(robot: tuple[Vec2, Vec2], R: int, C: int):
    p, v = robot
    p += v
    return Vec2(p.r % R, p.c % C), v


def count_neighbors(start: Vec2, robots: set[Vec2]):
    q = deque([start])
    visited = set()
    while q:
        p = q.popleft()
        if p in visited:
            continue
        visited.add(p)
        for d in RCDir.all:
            new = p+d
            if new in robots and new not in visited:
                q.append(new)
    return visited
