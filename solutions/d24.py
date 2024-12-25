import re
from lib import advent
from io import TextIOWrapper
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from typing import Self

GATE_FUNCTIONS = {
    'AND': lambda a, b: a & b,
    'OR': lambda a, b: a | b,
    'XOR': lambda a, b: a ^ b
}

@dataclass(init=False)
class Gate:
    a: str
    b: str
    op: Callable[[int, int], int]
    out: str
    waiting: bool
    opname: str

    def __init__(self, a, op, b, out):
        self.a = a
        self.b = b
        self.op = GATE_FUNCTIONS[op]
        self.out = out
        self.waiting = True
        self.opname = op

    def output(self, wires: defaultdict[str, int]):
        wires[self.out] = self.op(wires[self.a], wires[self.b])
        self.waiting = False
    
    def reset(self):
        self.waiting = True


@advent.parser(24)
def parse(file: TextIOWrapper):
    W, R = file.read().split('\n\n')
    wires = defaultdict(int)
    for line in W.splitlines():
        name, val = line.split(': ')
        wires[name] = int(val)
    rules = []
    for line in R.splitlines():
        a, op, b, _, out= line.split()
        rules.append(Gate(a, op, b, out))
    return wires, rules


@advent.solver(24, part=1)
def solve1(wires: defaultdict[str, int], rules: list[Gate]):
    return run(wires, rules)


@dataclass
class Node:
    a: Self | str
    b: Self | str


@advent.solver(24, part=2)
def solve2(_: defaultdict[str, int], rules: list[Gate]):
    invalid = []
    for i in range(2, 45):
        lines = walk(f'z{i:02}', {rule.out: rule for rule in rules}).splitlines()
        if 'XOR' not in lines[0]:
            invalid.append(lines[0].lstrip()[:3])
        elif 'AND' in lines[1] or 'XOR' in lines[1]:
            invalid.append(lines[1].lstrip()[:3])
        elif 'AND' not in lines[2]:
            invalid.append(lines[2].lstrip()[:3])
        elif 'AND' not in lines[4]:
            invalid.append(lines[4].lstrip()[:3])
        elif 'XOR' not in lines[7]:
            invalid.append(lines[7].lstrip()[:3])
    return ','.join(sorted([i for i in invalid if not i.startswith(('x', 'y'))]))


def walk(wire: str, rules: dict[str, Gate], goal: int = 0, indent: int = 0, depth: int = 3):
    if depth == 0:
        return ''
    s = (' '*indent) + wire + '='
    if 'x' in wire or 'y' in wire:
        return s[:-1] + '\n'
    rule = rules[wire]
    s += f'{rule.opname}(\n'
    if rule.a not in rules:
        s += walk(rule.a, rules, goal, indent+2, depth-1)
        s += walk(rule.b, rules, goal, indent+2, depth-1)
    else:
        match (rules[rule.a].opname, rules[rule.b].opname):
            case ('XOR', 'AND'):
                s += walk(rule.a, rules, goal, indent+2, depth-1)
                s += walk(rule.b, rules, goal, indent+2, depth-1)
            case ('AND', 'XOR'):
                s += walk(rule.b, rules, goal, indent+2, depth-1)
                s += walk(rule.a, rules, goal, indent+2, depth-1)
            case (_, 'OR'):
                s += walk(rule.b, rules, goal, indent+2, depth-1)
                s += walk(rule.a, rules, goal, indent+2, depth-1)
            case _, _:
                s += walk(rule.a, rules, goal, indent+2, depth-1)
                s += walk(rule.b, rules, goal, indent+2, depth-1)
    s += (' '*indent) + ')\n'
    return s


def run(wires: defaultdict[str, int], rules: list[Gate]):
    wires = wires.copy()
    while any(r.waiting for r in rules):
        for rule in rules:
            if rule.waiting and rule.a in wires and rule.b in wires:
                rule.output(wires)
    i = 0
    output = []
    while f'z{i:02}' in wires:
        output.append(str(wires[f'z{i:02}']))
        i += 1
    for r in rules:
        r.reset()
    return int(''.join(reversed(output)), base=2)
