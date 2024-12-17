import re
from lib import advent
from lib.common.vec import Vec2
from io import TextIOWrapper
from dataclasses import dataclass


@dataclass
class Machine:
    a: Vec2
    b: Vec2
    prize: Vec2


@advent.parser(13)
def parse(file: TextIOWrapper):
    prizes = []
    for group in file.read().split('\n\n'):
        vectors = []
        for line in group.splitlines():
            x, y = re.findall(r'\d+', line)
            vectors.append(Vec2(int(x), int(y)))
        prizes.append(Machine(*vectors))
    return prizes


@advent.solver(13, part=1)
def solve1(machines: list[Machine]):
    return sum(find_combo(machine.a, machine.b, machine.prize) for machine in machines)


@advent.solver(13, part=2)
def solve2(machines: list[Machine]):
    for machine in machines:
        machine.prize = Vec2(machine.prize.x + 10000000000000, machine.prize.y + 10000000000000)
    return sum(find_combo(prize.a, prize.b, prize.prize) for prize in machines)


def find_combo(a: Vec2, b: Vec2, p: Vec2):
    R = a.y / a.x
    B = round((p.y - R*p.x) / (b.y - R*b.x))
    A = round((p.x - B*b.x) / a.x)
    if A*a + B*b == p:
        return 3*A + B
    return 0
