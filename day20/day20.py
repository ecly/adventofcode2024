import copy
import sys
from collections import defaultdict, deque

filename = sys.argv[1] if len(sys.argv) > 1 else "test"
Coord = tuple[int, int]

cache: dict[tuple[Coord, Coord], int] = {}


def bfs(grid: list[list[str]], start: Coord, end: Coord) -> int | None:
    global cache
    if (start, end) in cache:
        return cache[start, end]

    queue: deque[tuple[int, Coord]] = deque([(0, start)])
    seen = set()
    while queue:
        dist, coord = queue.popleft()
        if coord in seen:
            continue

        cache[start, coord] = dist
        cache[coord, start] = dist
        if coord == end:
            return dist

        seen.add(coord)
        x, y = coord
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) in seen:
                continue

            if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
                continue

            if grid[ny][nx] == "#":
                continue

            queue.append((dist + 1, (nx, ny)))

    return None


def _find_value(grid, value) -> tuple[int, int]:
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == value:
                return x, y

    raise ValueError()


def get_path_coords(grid) -> list[Coord]:
    coords = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] != "#":
                coords.append((x, y))
    return coords


def manhatten(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def solve(grid, max_cheat, min_save):
    start = _find_value(grid, "S")
    end = _find_value(grid, "E")

    no_cheat_dist = bfs(grid, start, end)
    result = 0
    path_coords = get_path_coords(grid)
    saves = defaultdict(int)
    for cheat_start in path_coords:
        dist_from_start = bfs(grid, start, cheat_start)
        end_candidates = [
            p for p in path_coords if 1 < manhatten(cheat_start, p) <= max_cheat
        ]
        for cheat_end in end_candidates:
            dist_of_cheat = manhatten(cheat_start, cheat_end)
            dist_to_end = bfs(grid, cheat_end, end)
            total_dist = dist_from_start + dist_of_cheat + dist_to_end
            saved = no_cheat_dist - total_dist
            saves[saved] += 1

    return sum(count for saved, count in saves.items() if saved >= min_save)


def p1(grid):
    return solve(grid, 2, min_save=20 if filename == "test" else 100)


def p2(grid):
    return solve(grid, 20, min_save=50 if filename == "test" else 100)


grid = list(map(list, open(filename).read().strip().split("\n")))
print(p1(grid))
print(p2(grid))
