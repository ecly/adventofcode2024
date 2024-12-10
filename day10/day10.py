import sys
from collections import deque


def get_trails(grid, head_x, head_y):
    queue = deque([[(head_x, head_y, 0)]])
    paths = []
    while queue:
        path = queue.popleft()
        x, y, height = path[-1]
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            nx, ny = x + dx, y + dy
            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                continue

            n_height = grid[ny][nx]
            if grid[ny][nx] == height + 1:
                new_path = path + [(nx, ny, n_height)]
                if n_height == 9:
                    paths.append(new_path)
                else:
                    queue.append(new_path)
    return paths


def p1(grid, heads):
    score = 0
    for hx, hy in heads:
        trails = get_trails(grid, hx, hy)
        score += len({p[-1] for p in trails})

    return score


def p2(grid, heads):
    return sum(len(get_trails(grid, hx, hy)) for hx, hy in heads)


filename = "input" if len(sys.argv) == 1 else sys.argv[1]
grid = [[int(c) for c in row] for row in open(filename).read().strip().split("\n")]
heads = []
for y, row in enumerate(grid):
    for x, c in enumerate(row):
        if c == 0:
            heads.append((x, y))

print(p1(grid, heads))
print(p2(grid, heads))
