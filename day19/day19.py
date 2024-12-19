import copy
import sys
from collections import deque
from functools import lru_cache


@lru_cache(maxsize=1 << 16)
def possible_combinations(pattern: str, towels: tuple[str]) -> int:
    if not pattern:
        return 1

    return sum(
        possible_combinations(pattern[len(t) :], towels)
        for t in towels
        if pattern.startswith(t)
    )


def p1(patterns: list[str], towels: tuple[str, ...]):
    return sum(bool(possible_combinations(p, towels)) for p in patterns)


def p2(patterns: list[str], towels: tuple[str, ...]):
    return sum(possible_combinations(p, towels) for p in patterns)


filename = sys.argv[1] if len(sys.argv) > 1 else "test"
towels_str, patterns_str = open(filename).read().strip().split("\n\n")
towels = tuple(towels_str.split(", "))
patterns = patterns_str.split("\n")
print(p1(patterns, towels))
print(p2(patterns, towels))
