from collections import defaultdict, deque


def is_ordered(update: list[int], rules: dict[int, list[int]]) -> bool:
    seen: set[int] = set()
    for n in update:
        for before in rules[n]:
            if before in update and before not in seen:
                return False
        seen.add(n)

    return True


def reorder(update: list[int], rules: dict[int, list[int]]) -> list[int]:
    queue: deque[int] = deque(update)
    fixed = []
    while queue:
        n = queue.popleft()
        if any(r in update and r not in fixed for r in rules[n]):
            queue.append(n)
        else:
            fixed.append(n)

    return fixed


def part1(updates: list[list[int]], rules: dict[int, list[int]]) -> int:
    ordered_updates = [u for u in updates if is_ordered(u, rules)]
    return sum(u[len(u) // 2] for u in ordered_updates)


def part2(updates: list[list[int]], rules: dict[int, list[int]]) -> int:
    unordered_updates = [u for u in updates if not is_ordered(u, rules)]
    reordered_updates = [reorder(u, rules) for u in unordered_updates]
    return sum(u[len(u) // 2] for u in reordered_updates)


rules_str, updates_str = open("input").read().strip().split("\n\n")
rules = defaultdict(list)
for rule in rules_str.split("\n"):
    left, right = rule.split("|")
    rules[int(right)].append(int(left))

print(updates_str)
updates = [list(map(int, u.split(","))) for u in updates_str.split("\n")]
print(part1(updates, rules))
print(part2(updates, rules))
