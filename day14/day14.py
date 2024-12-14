import math
import re
import sys
from collections import Counter, deque

filename = sys.argv[1] if len(sys.argv) > 1 else "test"
MAX_X = 101 if filename == "input" else 11
MAX_Y = 103 if filename == "input" else 7


def visualize(robots):
    counter = Counter([(x, y) for x, y, _, _ in robots])
    for y in range(MAX_Y):
        for x in range(MAX_X):
            print(counter.get((x, y)) or ".", end="")

        print()


def safety_factor(robots):
    quadrants = [0, 0, 0, 0]
    cutoff_x, cutoff_y = MAX_X // 2, MAX_Y // 2
    for r in robots:
        rx, ry, _, _ = r
        # in between quadrants
        if rx == cutoff_x or ry == cutoff_y:
            continue
        if rx < cutoff_x:
            if ry < cutoff_y:
                quadrants[0] += 1
            else:
                quadrants[2] += 1
        else:
            if ry < cutoff_y:
                quadrants[1] += 1
            else:
                quadrants[3] += 1

    print(quadrants)
    return math.prod(quadrants)


def simulate(robots, seconds):
    def step(robot, s):
        rx, ry, dx, dy = robot
        return (rx + dx * s) % MAX_X, (ry + dy * s) % MAX_Y, dx, dy

    return [step(r, seconds) for r in robots]


def p1(robots):
    return safety_factor(simulate(robots, 100))


def largest_connection(robots):
    rs = {(x, y) for x, y, _, _ in robots}
    seen = set()
    groups = []
    for r in rs:
        if r in seen:
            continue
        queue = deque([r])
        group = {r}
        while queue:
            robot = queue.popleft()
            (
                x,
                y,
            ) = robot
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                nx, ny = x + dx, y + dy
                if (nx, ny) in rs and (nx, ny) not in group:
                    queue.append((nx, ny))
                    group.add((nx, ny))

        seen.update(group)
        groups.append(group)

    return max(len(g) for g in groups)


def p2(robots):
    for s in range(1, 100000):
        robots = simulate(robots, 1)
        max_conn = largest_connection(robots)
        if max_conn > 30:
            visualize(robots)
            return s

    return None


lines = open(filename).read().strip().split("\n")
robots = [tuple(map(int, re.findall("-?\d+", line))) for line in lines]

print(p1(robots))
print(p2(robots))
