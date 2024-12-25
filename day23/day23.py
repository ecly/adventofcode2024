import copy
import sys
from collections import defaultdict, deque

filename = sys.argv[1] if len(sys.argv) > 1 else "test"


def find_3_sets(conns: defaultdict[str, set[str]]):
    pools = set()
    for n1 in conns:
        for n2 in conns[n1]:
            for n3 in conns[n2]:
                if n1 in conns[n3]:
                    pools.add((tuple(sorted([n1, n2, n3]))))

    return pools


def find_largest_set(conns: defaultdict[str, set[str]]):
    seen: set[str] = set()
    largest_set: set[str] = set()

    for node in conns:
        pool = {node}
        queue = deque(conns[node])
        while queue:
            n = queue.popleft()
            if len(pool & conns[n]) == len(pool):
                pool.add(n)

        if len(pool) > len(largest_set):
            largest_set = pool

    return largest_set


def p1(conns):
    sets = find_3_sets(conns)
    return len([s for s in sets if any(c.startswith("t") for c in s)])


def p2(conns):
    largest = find_largest_set(conns)
    return ",".join(sorted(largest))


conns = defaultdict(set)
for line in open(filename).read().strip().split("\n"):
    a, b = line.split("-")
    conns[a].add(b)
    conns[b].add(a)


print(p1(conns))
print(p2(conns))
