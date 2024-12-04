def get_diagonals(matrix: list[str]) -> list[str]:
    rows, cols = len(matrix), len(matrix[0])
    diagonals = []
    # Forward diagonals
    for d in range(-(rows - 2), cols - 1):
        diagonal = [
            matrix[i][j] for i in range(rows) for j in range(cols) if i - j == d
        ]
        if len(diagonal) > 1:
            diagonals.append("".join(diagonal))

    # Backward diagonals
    for d in range(rows + cols - 3):
        diagonal = [
            matrix[i][j] for i in range(rows) for j in range(cols) if i + j == d
        ]
        if len(diagonal) > 1:
            diagonals.append("".join(diagonal))

    return diagonals


def count_xmas(lines: list[str]) -> int:
    transposed = list(map(lambda x: "".join(x), zip(*lines)))
    return sum(
        line.count("XMAS") + line[::-1].count("XMAS")
        for line in lines + transposed + get_diagonals(lines)
    )


def count_x_mas(lines: list[str]) -> int:
    count = 0
    x_mas_patterns = {"MASMAS", "MASSAM", "SAMMAS", "SAMSAM"}
    for start_x in range(len(lines[0]) - 2):
        for start_y in range(len(lines) - 2):
            patch = []
            for dx, dy in [(0, 0), (1, 1), (2, 2), (0, 2), (1, 1), (2, 0)]:
                patch.append(lines[start_x + dx][start_y + dy])

            patch_str = "".join(patch)
            if patch_str in x_mas_patterns:
                count += 1

    return count


lines = open("input").read().strip().split("\n")
print(count_xmas(lines))
print(count_x_mas(lines))
