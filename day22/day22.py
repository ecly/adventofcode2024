import copy
import sys
from collections import defaultdict, deque
from functools import lru_cache, reduce
from statistics import mean


def mix(a: int, b: int) -> int:
    return a ^ b


def prune(a: int) -> int:
    return a % 16777216


def next_secret(s: int) -> int:
    s1 = prune(mix(s, s * 64))
    s2 = prune(mix(s1, s1 // 32))
    s3 = prune(mix(s2, s2 * 2048))
    return s3


def p1(secrets: list[int]) -> int:
    result = 0
    for s in secrets:
        for _ in range(2000):
            s = next_secret(s)

        result += s

    return result


def p2(secrets: list[int]) -> int:
    x: defaultdict[tuple[int, ...], list[int]] = defaultdict(list)
    for s in secrets:
        hist = [s]
        deltas = []
        seen = set()
        for i in range(2000):
            ns = next_secret(hist[-1])
            delta = (ns % 10) - (hist[-1] % 10)
            deltas.append(delta)
            if len(deltas) >= 4:
                last_4 = tuple(deltas[-4:])
                if last_4 not in seen:
                    seen.add(last_4)
                    x[last_4].append(ns % 10)
            hist.append(ns)

    return max(sum(v) for v in x.values())


filename = sys.argv[1] if len(sys.argv) > 1 else "test"
secrets = list(map(int, open(filename).read().strip().split("\n")))
print(p1(secrets))
print(p2(secrets))
