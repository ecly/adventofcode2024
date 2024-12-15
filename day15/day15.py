import re
import sys

Grid = list[list[str]]
Ops = list[tuple[int, int]]


def parse(input_: str) -> tuple[Grid, Ops]:
    g, o = input_.strip().split("\n\n")
    grid = list(map(list, g.split("\n")))
    ops_map = {"<": (-1, 0), "^": (0, -1), ">": (1, 0), "v": (0, 1)}
    ops = [ops_map[op] for op in re.sub("\s", "", o)]
    return grid, ops


def _find_robot(grid) -> tuple[int, int]:
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] == "@":
                return x, y

    raise ValueError()


def can_move(grid: Grid, item: tuple[int, int], op: tuple[int, int]) -> bool:
    x, y = item
    dx, dy = op
    nx, ny = x + dx, y + dy
    n = grid[ny][nx]
    if n == "#":
        return False

    if n == ".":
        return True

    if n == "O":
        return can_move(grid, (nx, ny), op)

    if n == "[":
        # if moving left side of bozz vertically, we need to check if entire box can move
        if dy:
            return can_move(grid, (nx, ny), op) and can_move(grid, (nx + 1, ny), op)

        return can_move(grid, (nx, ny), op)

    if n == "]":
        # if moving right side of bozz vertically, we need to check if entire box can move
        if dy:
            return can_move(grid, (nx, ny), op) and can_move(grid, (nx - 1, ny), op)

        return can_move(grid, (nx, ny), op)

    return False


def move(grid: Grid, item: tuple[int, int], op: tuple[int, int]) -> tuple[int, int]:
    x, y = item
    dx, dy = op
    nx, ny = x + dx, y + dy
    n = grid[ny][nx]
    assert grid[y][x] in "O@[]"

    # Move chain of boxes
    if n == "O":
        move(grid, (nx, ny), op)

    if n == "[":
        if dy:
            move(grid, (nx, ny), op)
            move(grid, (nx + 1, ny), op)
        else:
            move(grid, (nx, ny), op)

    if n == "]":
        if dy:
            move(grid, (nx, ny), op)
            move(grid, (nx + -1, ny), op)
        else:
            move(grid, (nx, ny), op)

    grid[ny][nx] = grid[y][x]
    grid[y][x] = "."

    return nx, ny


def try_move(grid: Grid, item: tuple[int, int], op: tuple[int, int]) -> tuple[int, int]:
    # we only execute a chain of moves if we're sure that the chain will fully succeed.
    if can_move(grid, item, op):
        return move(grid, item, op)
    return item


def run_ops(grid: Grid, ops: Ops):
    x, y = _find_robot(grid)
    for op in ops:
        if can_move(grid, (x, y), op):
            x, y = move(grid, (x, y), op)


def gps_coords(grid):
    result = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in ("[", "O"):
                result += 100 * y + x

    return result


def solve(input_: str):
    grid, ops = parse(input_)
    x, y = _find_robot(grid)
    for op in ops:
        x, y = try_move(grid, (x, y), op)
    return gps_coords(grid)


def p1(filename: str):
    return solve(open(filename).read())


def p2(filename: str):
    input_ = open(filename).read()
    input_ = input_.replace("O", "[]")
    input_ = input_.replace("#", "##")
    input_ = input_.replace(".", "..")
    input_ = input_.replace("@", "@.")
    return solve(input_)


filename = sys.argv[1] if len(sys.argv) > 1 else "test"
print(p1(filename))
print(p2(filename))
