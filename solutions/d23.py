from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict


@advent.parser(23)
def parse(file: TextIOWrapper):
    connections = defaultdict(set)
    for line in file.readlines():
        a, b = line.strip().split('-')
        connections[a].add(b)
        connections[b].add(a)
    return connections


@advent.solver(23, part=1)
def solve1(connections: defaultdict[str, set[str]]):
    valid = set()
    for src in connections:
        q = deque([(src, list())])
        while q:
            curr, path = q.pop()
            if len(path) == 3 and curr == path[0]:
                if any('t' == comp[0] for comp in path):
                    valid.add(tuple(sorted(path)))
                continue
            if len(path) == 3 or curr in path:
                continue
            for dst in connections[curr]:
                q.append((dst, path + [curr]))
    return len(valid)


@advent.solver(23, part=2)
def solve2(connections: defaultdict[str, set[str]]):
    best = set()
    for src in connections:
        subset = bron_kerbosch({src}, connections[src], set(), connections)
        if len(subset) > len(best):
            best = subset
    return ','.join(sorted(best))


def bron_kerbosch(
    subset: set[str],
    possible_connections: set[str],
    impossible_connections: set[str],
    connections: defaultdict[str, set[str]]
):
    if not possible_connections and not impossible_connections:
        return subset
    best = set()
    for v in set(possible_connections):
        new = bron_kerbosch(
            subset | {v},
            possible_connections & connections[v],
            impossible_connections & connections[v],
            connections
        )
        if len(new) > len(best):
            best = new
        possible_connections -= {v}
        impossible_connections |= {v}
    return best
