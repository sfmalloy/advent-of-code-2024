import re
from lib import advent
from io import TextIOWrapper


@advent.parser(3)
def parse(file: TextIOWrapper):
    return file.read().strip()


@advent.solver(3, part=1)
def solve1(prog: str):
    ans = 0
    for mul in re.finditer(r'mul\((\d+),(\d+)\)', prog):
        a, b = map(int, mul.groups())
        ans += a * b
    return ans


@advent.solver(3, part=2, reparse=False)
def solve2(prog: str):
    ans = 0
    enabled = True
    for mul in re.finditer(r"(?P<action>do(n't)?)\(\)|(mul)\((?P<a>\d+),(?P<b>\d+)\)", prog):
        groups = mul.groupdict()
        match groups['action']:
            case 'do':
                enabled = True
            case "don't":
                enabled = False
            case _:
                if enabled:
                    a, b = int(groups['a']), int(groups['b'])
                    ans += a * b
    return ans
