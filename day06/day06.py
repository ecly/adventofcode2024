import copy


def guard_walk(grid, x, y, dx, dy) -> list[tuple[int, int, int, int]]:
    path = [(x, y, dx, dy)]
    while True:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
            break

        if grid[ny][nx] == "#":
            dx, dy = dy * -1, dx
        else:
            x, y = nx, ny
            path.append((x, y, dx, dy))

    return path


def check_loop(grid, x, y, dx, dy) -> bool:
    seen = {(x, y, dx, dy)}
    turns = 0
    while True:
        nx, ny = x + dx, y + dy
        if not (0 <= nx < len(grid[0]) and 0 <= ny < len(grid)):
            return False

        if grid[ny][nx] == "#":
            dx, dy = dy * -1, dx
            turns += 1
        else:
            x, y = nx, ny

        if (x, y, dx, dy) in seen:
            return True

        seen.add((x, y, dx, dy))

    return False


def part1(lines, x, y) -> int:
    dx, dy = 0, -1
    path = guard_walk(lines, x, y, dx, dy)
    return len({(x, y) for x, y, _, _ in path})


def part2(lines, x, y) -> int:
    dx, dy = 0, -1
    # only need to check positions on the existing path.
    positions = guard_walk(lines, x, y, dx, dy)
    loop_obstacles = set()
    for ox, oy in {(px, py) for px, py, _, _ in positions}:
        if (ox, oy) == (x, y) or (ox, oy) in loop_obstacles:
            continue
        loop_grid = copy.deepcopy(grid)
        loop_grid[oy][ox] = "#"
        if check_loop(loop_grid, x, y, dx, dy):
            loop_obstacles.add((ox, oy))

    return len(loop_obstacles)


text = open("input").read().strip()
start_idx = text.replace("\n", "").index("^")
grid = list(map(list, text.replace("^", ".").split("\n")))
x = start_idx % len(grid[0])
y = start_idx // len(grid)
print(part1(grid, x, y))
print(part2(grid, x, y))
