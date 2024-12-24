from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
from collections.abc import Callable
from dataclasses import dataclass

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

    def __init__(self, a, op, b, out):
        self.a = a
        self.b = b
        self.op = GATE_FUNCTIONS[op]
        self.out = out
        self.waiting = True

    def output(self, wires: defaultdict[str, int]):
        wires[self.out] = self.op(wires[self.a], wires[self.b])
        self.waiting = False


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
    while any(rule.waiting for rule in rules):
        for rule in rules:
            if rule.waiting and rule.a in wires and rule.b in wires:
                rule.output(wires)
    i = 0
    output = []
    while f'z{i:02}' in wires:
        output.append(str(wires[f'z{i:02}']))
        i += 1
    return int(''.join(reversed(output)), base=2)


@advent.solver(24, part=2)
def solve2(wires: defaultdict[str, int], rules: list[Gate]):
    output_to_rule = {rule.out: rule for rule in rules}
    xy_size = 0
    # for r in rules:
    #     if 'x' in r.a:
    #         xy_size = max(xy_size, int(r.a[1:]))
    #     elif 'x' in r.b:
    #         xy_size = max(xy_size, int(r.b[1:]))
    for k,v in output_to_rule.items():
        if 'z' in v.out:
            print(v.out)
            find_z(v.a, rules, int(v.out[1:]), 2)
            find_z(v.b, rules, int(v.out[1:]), 2)
    return 0


def find_z(wire: str, rules: list[Gate], goal: int, indent=0):
    if 'z' in wire or 'x' in wire or 'y' in wire:
        return int(wire[1:]) == goal
    for w in rules:
        if w.out == wire:
            if find_z(w.a, rules, indent + 2) or find_z(w.b, rules, goal, indent + 2):
                return True
    return False
    # print(wire)
    # find_z(output_to_rule[wire].a, wires, output_to_rule, indent + 2)
    # print(wire)
    # find_z(output_to_rule[wire].b, wires, output_to_rule, indent + 2)
