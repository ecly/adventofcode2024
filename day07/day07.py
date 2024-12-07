from collections import deque
from operator import add, mul


def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))


def is_solvable(r: int, nums: list[int], ops: list) -> bool:
    queue = deque([(nums[0], nums[1:])])
    while queue:
        s, ns = queue.popleft()
        if not ns:
            if s == r:
                return True
            continue

        head, nss = ns[0], ns[1:]
        for op in ops:
            queue.append((op(s, head), nss))
    return False


def solve(eqs: list[tuple[int, list[int]]], ops: list):
    total_result = 0
    for result, nums in eqs:
        if is_solvable(result, nums, ops):
            total_result += result

    return total_result


def p1(eqs: list[tuple[int, list[int]]]):
    return solve(eqs, [add, mul])


def p2(eqs: list[tuple[int, list[int]]]):
    return solve(eqs, [add, mul, concat])


lines = open("input").read().strip().split("\n")
eqs = []
for line in lines:
    print(line)
    result, nums = line.split(": ")
    eqs.append((int(result), list(map(int, nums.split()))))

print(p1(eqs))
print(p2(eqs))
