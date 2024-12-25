from lib import advent
from io import TextIOWrapper


@advent.parser(25)
def parse(file: TextIOWrapper):
    locks_and_keys = file.read().split('\n\n')
    keys = []
    locks = []
    for group in locks_and_keys:
        if group[0] == '#':
            locks.append([pin.count('#') - 1 for pin in list(zip(*group.splitlines()))])
        else:
            keys.append([pin.count('#') - 1 for pin in list(zip(*group.splitlines()))])
    return keys, locks


@advent.solver(25, part=1)
def solve1(keys: list[list[str]], locks: list[list[str]]):
    pairs = set()
    for i, lock in enumerate(locks):
        for k, key in enumerate(keys):
            if fit_key(lock, key):
                pairs.add((i, k))
    return len(pairs)


@advent.solver(25, part=2)
def solve2(_, __):
    return 'Merry Christmas!'


def fit_key(lock: tuple[int], key: tuple[int]):
    for kp, lp in zip(lock, key):
        if kp + lp >= 6:
            return False
    return True
