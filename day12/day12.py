import sys
from collections import defaultdict, deque

Grid = list[list[str]]
Region = set[tuple[int, int]]


def find_region(grid: Grid, start_x: int, start_y: int) -> Region:
    queue = deque([(start_x, start_y)])
    c = grid[start_y][start_x]
    region: set[tuple[int, int]] = {(start_x, start_y)}
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            nx, ny = x + dx, y + dy
            if (
                (nx, ny) in region
                or not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid))
                or grid[ny][nx] != c
            ):
                continue

            region.add((nx, ny))
            queue.append((nx, ny))
    return region


def find_regions(grid: Grid) -> list[Region]:
    seen: set[tuple[int, int]] = set()
    regions = []
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in seen:
                continue

            region = find_region(grid, x, y)
            regions.append(region)
            seen.update(region)

    return regions


def calculate_perimeter(region: Region) -> int:
    perimeter = 0
    for x, y in region:
        for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
            nx, ny = x + dx, y + dy
            if (nx, ny) not in region:
                perimeter += 1

    return perimeter


def p1(grid: Grid) -> int:
    regions = find_regions(grid)
    return sum(len(r) * calculate_perimeter(r) for r in regions)


def count_disjoint(ns: list[int]):
    sections = 0
    cont: list[int] = []
    for i in sorted(ns):
        if not cont:
            cont.append(i)
        elif i - cont[-1] == 1:
            cont.append(i)
        else:
            cont = [i]
            sections += 1
    if cont:
        sections += 1

    return sections


def count_sides(region: Region) -> int:
    sides = 0

    min_x = min(x for x, _ in region)
    max_x = max(x for x, _ in region)
    min_y = min(y for _, y in region)
    max_y = max(y for _, y in region)

    # Horizontal sides
    y_sides = defaultdict(list)
    for y in range(min_y - 1, max_y + 1):
        prev_in_shape = False
        for x in range(min_x - 1, max_x + 2):
            current_in_shape = (x, y) in region
            if current_in_shape != prev_in_shape:
                sides += 1
                # track inside/outside fence separately.
                y_sides[x, current_in_shape].append(y)
            prev_in_shape = current_in_shape

    # Vertical sides
    x_sides = defaultdict(list)
    for x in range(min_x, max_x + 1):
        prev_in_shape = False
        for y in range(min_y - 1, max_y + 2):
            current_in_shape = (x, y) in region
            if current_in_shape != prev_in_shape:
                sides += 1
                # track inside/outside fence separately.
                x_sides[y, current_in_shape].append(x)
            prev_in_shape = current_in_shape

    x_sides_cont = sum(count_disjoint(v) for v in x_sides.values())
    y_sides_cont = sum(count_disjoint(v) for v in y_sides.values())
    return y_sides_cont + x_sides_cont


def p2(grid: Grid) -> int:
    regions = find_regions(grid)
    return sum(len(r) * count_sides(r) for r in regions)


filename = sys.argv[1] if len(sys.argv) > 1 else "test"
lines = list(map(list, open(filename).read().strip().split("\n")))
print(p1(lines))
print(p2(lines))
