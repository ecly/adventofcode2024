from collections import defaultdict
from itertools import combinations

lines = open("input").read().strip().split("\n")


def p1(antennas):
    antinodes = set()
    for frequency in antennas.values():
        for (ax, ay), (bx, by) in combinations(frequency, 2):
            dx, dy = ax - bx, ay - by
            antinodes.add((ax + dx, ay + dy))
            antinodes.add((bx - dx, by - dy))

    within_map = [
        (x, y) for (x, y) in antinodes if 0 <= x < len(lines[0]) and 0 <= y < len(lines)
    ]
    return len(within_map)


def p2(antennas):
    antinodes = set()
    for frequency in antennas.values():
        for (ax, ay), (bx, by) in combinations(frequency, 2):
            # the antennas themself that have at least two of th frequency
            # are antinodes themself
            antinodes.add((ax, ay))
            antinodes.add((bx, by))
            dx, dy = ax - bx, ay - by
            i = 1
            while True:
                nx, ny = ax + (i * dx), ay + (i * dy)
                if not (0 <= nx < len(lines[0]) and 0 <= ny < len(lines)):
                    break
                antinodes.add((nx, ny))
                i += 1

            i = 1
            while True:
                nx, ny = bx - (i * dx), by - (i * dy)
                if not (0 <= nx < len(lines[0]) and 0 <= ny < len(lines)):
                    break
                antinodes.add((nx, ny))
                i += 1

    return len(antinodes)


antennas = defaultdict(list)
for y, line in enumerate(lines):
    for x, c in enumerate(line):
        if c.isdigit() or c.isalpha():
            antennas[c].append((x, y))

print(p1(antennas))
print(p2(antennas))
