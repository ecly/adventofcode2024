import copy
import sys
from collections import deque

filename = sys.argv[1] if len(sys.argv) > 1 else "test"
BYTES_TO_SIMULATE = 1024 if filename == "input" else 12
WIDTH = 71 if filename == "input" else 7
HEIGHT = WIDTH
Coord = tuple[int, int]


def visualize(grid):
    for row in grid:
        print("".join("#" if corrupted else "." for corrupted in row))


def bfs(grid, start, end) -> list[Coord]:
    queue: deque[tuple[Coord, list[Coord]]] = deque([(start, [])])
    seen = set()
    while queue:
        c, path = queue.popleft()
        if c in seen:
            continue

        seen.add(c)
        if c == end:
            return path

        new_path = path + [c]
        x, y = c
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                continue
            if grid[ny][nx]:
                continue

            queue.append(((nx, ny), new_path))

    return []


def p1(grid, corrupted_bytes):
    grid = copy.deepcopy(grid)
    for x, y in corrupted_bytes[:BYTES_TO_SIMULATE]:
        grid[y][x] = True

    dist = bfs(grid, (0, 0), (WIDTH - 1, HEIGHT - 1))
    return len(dist)


def p2(grid, corrupted_bytes):
    grid = copy.deepcopy(grid)
    for x, y in corrupted_bytes[:BYTES_TO_SIMULATE]:
        grid[y][x] = True

    for i, (x, y) in enumerate(corrupted_bytes[BYTES_TO_SIMULATE:], BYTES_TO_SIMULATE):
        grid[y][x] = True
        if not bfs(grid, (0, 0), (WIDTH - 1, HEIGHT - 1)):
            return f"{x},{y}"

    return None


grid = [[False for _ in range(WIDTH)] for _ in range(HEIGHT)]
corrupted_bytes = []
for l in open(filename).read().strip().split("\n"):
    x, y = map(int, l.split(","))
    corrupted_bytes.append((x, y))


print(p1(grid, corrupted_bytes))
print(p2(grid, corrupted_bytes))
