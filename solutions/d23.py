from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict
from itertools import permutations


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
    depth = 4
    while True:
        found = find_connections(depth, connections) 
        if len(found) == 1:
            return ','.join(found.pop())
        depth += 1


def find_connections(depth: int, connections: defaultdict[str, set]):
    valid = set()
    visited = set()
    for src in connections:
        q = deque([(src, {src})])
        while q:
            curr, path = q.pop()
            if len(path) == depth:
                valid.add(tuple(sorted(path)))
                if len(valid) > 1:
                    return valid
                continue
            if (curr, tuple(sorted(path))) in visited:
                continue
            visited.add((curr, tuple(sorted(path))))
            for dst in connections[curr]:
                if (dst, tuple(sorted(path | {dst}))) in visited:
                    continue
                if not path or connections[dst] & path == path:
                    q.append((dst, path | {dst}))
    return valid
