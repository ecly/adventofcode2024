import sys

A_COST = 3
B_COST = 1


def cost_of_win_man(a, b, prize):
    # Written by hand for p1 under the constraints of the 100 presses max
    ax, ay = a
    bx, by = b
    px, py = prize

    cheapest = None
    for a_presses in range(100):
        x_rem = px - (ax * a_presses)
        y_rem = py - (ay * a_presses)
        if x_rem < 0 or y_rem < 0:
            break
        if x_rem % bx == 0 and y_rem % by == 0 and x_rem // bx == y_rem // by:
            cost = a_presses * A_COST + (x_rem // bx) * B_COST
            if cheapest is None or cost < cheapest:
                cheapest = cost

    return 0 if cheapest is None else cheapest


def cost_of_win_machine(a, b, prize) -> int:
    # Written with the aid of Claude 3.5 Sonnet because i'm bad at math
    ax, ay = a
    bx, by = b
    px, py = prize

    # Main determinant
    D = (ax * by) - (bx * ay)

    # Determinant for A
    Da = (px * by) - (bx * py)

    # Determinant for B
    Db = (ax * py) - (px * ay)

    # No prize
    if Da % D != 0 or Db % D != 0:
        return 0

    A = Da / D
    B = Db / D

    return int(A * A_COST + B * B_COST)


def p1(machines):
    return sum(cost_of_win_man(*m) for m in machines)


def p2(machines):
    extra = 10000000000000
    return sum(
        cost_of_win_machine(a, b, (px + extra, py + extra))
        for a, b, (px, py) in machines
    )


filename = sys.argv[1] if len(sys.argv) > 1 else "test"
sections = open(filename).read().strip().split("\n\n")

machines: list[tuple[tuple[int, int], tuple[int, int], tuple[int, int]]] = []
for section in sections:

    def parse(s):
        x, y = 0, 0
        for d in s.replace("=", "").split(": ")[1].split(", "):
            if d.startswith("X"):
                x += int(d[1:])
            else:
                y += int(d[1:])
        return x, y

    axy, bxy, prize_xy = map(parse, section.split("\n"))
    machines.append((axy, bxy, prize_xy))

# 85210 is too high
print(p1(machines))
print(p2(machines))
