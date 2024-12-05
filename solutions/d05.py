from lib import advent
from io import TextIOWrapper
from collections import defaultdict
from functools import cmp_to_key


@advent.parser(5)
def parse(file: TextIOWrapper) -> tuple[defaultdict[int, list], list[list[int]]]:
    rule_lines, case_lines = file.read().split('\n\n')
    rules = defaultdict(set)
    for rule in rule_lines.splitlines():
        x, y = map(int, rule.split('|'))
        # rule y must have x BEFORE it
        rules[y].add(x)
    updates = [list(map(int, c.split(','))) for c in case_lines.splitlines()]
    return rules, updates


@advent.solver(5, part=1)
def solve1(rules: defaultdict[int, list], updates: list[list[int]]):
    ans = 0
    for update in updates:
        if check_update(rules, update):
            ans += update[len(update)//2]
    return ans


@advent.solver(5, part=2)
def solve2(rules: defaultdict[int, list], updates: list[list[int]]):
    ans = 0
    for update in updates:
        if not check_update(rules, update):
            ans += sorted(update, key=cmp_to_key(lambda p, b: -1 if b in rules[p] else 0))[len(update)//2]
    return ans


def check_update(rules: defaultdict[int, list], update: list[int]):
    for p, page in enumerate(update):
        for before in update[p+1:]:
            if before in rules[page]:
                return False
    return True
