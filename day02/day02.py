import copy
import sys


def _is_safe(reports: list[int], allowed_skips: int = 0):
    i = 0
    for i in range(len(reports) - 1):
        l, h = reports[i], reports[i + 1]
        if 1 <= h - l <= 3:
            i += 1
            continue

        return False

    return True


def is_safe(reports: list[int]) -> bool:
    return _is_safe(reports) or _is_safe(reports[::-1])


def is_safe2(reports: list[int]):
    if is_safe(reports):
        return True

    for i in range(len(reports)):
        r = copy.copy(reports)
        r.pop(i)
        if is_safe(r):
            return True

    return False



reports = [list(map(int, l.split())) for l in sys.stdin.readlines()]
print(sum(is_safe(r) for r in reports))
print(sum(is_safe2(r) for r in reports))
