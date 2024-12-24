import math
from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
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


# https://www.reddit.com/r/adventofcode/comments/1hla5ql/2024_day_24_part_2_a_guide_on_the_idea_behind_the/
# https://en.wikipedia.org/wiki/Adder_(electronics)#Ripple-carry_adder
# had to look up some hints from the reddit thread, and the wikipedia page has a nice ripple-carry adder diagram
@advent.solver(24, part=2)
def solve2(wires: defaultdict[str, int], rules: list[Gate]):
    invalid = []
    def find_op(src: str, opname: str):
        for r in rules:
            if (r.a == src or r.b == src) and r.opname == opname:
                return True
        return False

    for r in rules:
        if r.out == 'z45':
            continue
        if r.out.startswith('z') and r.opname != 'XOR':
            invalid.append(r.out)
        elif r.opname == 'AND' and r.a != 'x00' and not find_op(r.out, 'OR'):
            invalid.append(r.out)
        elif not r.out.startswith('z') and not r.a.startswith(('x', 'y')) and r.opname == 'XOR':
            invalid.append(r.out)
        elif r.opname == 'XOR' and r.a.startswith(('x', 'y')) and r.a != 'x00' and not find_op(r.out, 'XOR'):
            invalid.append(r.out)
    return ','.join(sorted(invalid))


def walk(wire: str, rules: dict[str, Gate], goal: int=0, indent=0, seen: frozenset=None):
    print((' '*indent) + wire, end='=')
    if not seen:
        seen = frozenset()
    if 'x' in wire or 'y' in wire:
        print()
        return
    rule = rules[wire]
    print(f'{rule.opname}(')
    if rule.a not in rules:
        walk(rule.a, rules, goal, indent+2)
        walk(rule.b, rules, goal, indent+2)
    else:
        match (rules[rule.a].opname, rules[rule.b].opname):
            case ('XOR', 'AND'):
                walk(rule.a, rules, goal, indent+2)
                walk(rule.b, rules, goal, indent+2)
            case ('AND', 'XOR'):
                walk(rule.b, rules, goal, indent+2)
                walk(rule.a, rules, goal, indent+2)
            case (_, 'OR'):
                walk(rule.b, rules, goal, indent+2)
                walk(rule.a, rules, goal, indent+2)
            case _, _:
                walk(rule.a, rules, goal, indent+2)
                walk(rule.b, rules, goal, indent+2)
    print((' '*indent) + ')')
    return seen


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
