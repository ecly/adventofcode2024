import copy
import sys
from collections import deque
from functools import lru_cache
from itertools import product

Key = tuple[int, ...]
Lock = tuple[int, ...]


def parse(filename) -> tuple[list[Key], list[Lock]]:
    keys = []
    locks = []
    for section in open(filename).read().strip().split("\n\n"):
        is_lock = section.startswith("#####")
        layout = [0] * 5
        lines = section.split("\n")
        if not is_lock:
            lines = lines[::-1]

        for height, line in enumerate(lines):
            for i in range(len(line)):
                if line[i] == "#":
                    layout[i] = height

        if is_lock:
            locks.append(tuple(layout))
        else:
            keys.append(tuple(layout))

    return keys, locks


def is_fit(key: Key, lock: Lock) -> bool:
    return all(k + l <= 5 for k, l in zip(key, lock))


def p1(keys: list[Key], locks: list[Lock]) -> int:
    return sum(is_fit(k, l) for k, l in product(keys, locks))


filename = sys.argv[1] if len(sys.argv) > 1 else "test"
keys, locks = parse(filename)
print(p1(keys, locks))
