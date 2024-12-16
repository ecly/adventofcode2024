import sys
from heapq import heappop, heappush


def shortest_paths(grid, start, end):
    start_x, start_y = start
    queue = [(0, start_x, start_y, 1, 0, [])]
    seen = {}
    found = []
    while queue:
        item = heappop(queue)
        cost, x, y, dx, dy, path = item
        if (x, y) == end:
            found.append((cost, path + [(x, y, dx, dy)]))

        if found and cost > found[-1][0]:
            break

        if seen.get((x, y, dx, dy), float("inf")) < cost:
            continue

        seen[x, y, dx, dy] = cost
        new_path = path + [(x, y, dx, dy)]
        nx, ny = x + dx, y + dy
        if grid[ny][nx] != "#":
            heappush(queue, (cost + 1, nx, ny, dx, dy, new_path))

        # turn right
        heappush(queue, (cost + 1000, x, y, dy * -1, dx, new_path))

        # turn left
        heappush(queue, (cost + 1000, x, y, dy, dx * -1, new_path))

    return found


def p1(grid, start, end):
    cost, _ = shortest_paths(grid, start, end)[0]
    return cost


def p2(grid, start, goal):
    paths = shortest_paths(grid, start, end)
    return len({(x, y) for _, path in paths for x, y, _, _ in path})


filename = sys.argv[1] if len(sys.argv) > 1 else "test"
grid = open(filename).read().strip().split("\n")
start = 1, len(grid) - 2
end = len(grid[0]) - 2, 1
print(p1(grid, start, end))
print(p2(grid, start, end))
