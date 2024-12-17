import re
import sys


def run(a, b, c, ns, max_outputs=1 << 8):
    def combo(i):
        if i <= 3:
            return i
        if i == 4:
            return a
        if i == 5:
            return b
        if i == 6:
            return c
        assert i != 7, "Not in valid programs"
        raise ValueError()

    outputs = []
    pt = 0
    # halts when read past the program
    while 0 <= pt < len(ns) and len(outputs) <= max_outputs:
        opcode = ns[pt]
        if opcode == 0:  # adv
            a = a // (2 ** combo(ns[pt + 1]))
        elif opcode == 1:  # bxl
            # bitwise xor
            b = b ^ ns[pt + 1]
        elif opcode == 2:  # bst
            b = combo(ns[pt + 1]) % 8
        elif opcode == 3:  # jnz
            if a != 0:
                pt = ns[pt + 1]
                # don't increment pt on successful jump
                continue
        elif opcode == 4:  # bxc
            b = b ^ c
        elif opcode == 5:  # out
            # print(combo(ns[pt + 1]))
            outputs.append(combo(ns[pt + 1]) % 8)
        elif opcode == 6:  # bdv
            b = a // (2 ** combo(ns[pt + 1]))
        elif opcode == 7:  # cdv
            c = a // (2 ** combo(ns[pt + 1]))

        pt += 2

    return outputs


def p1(a, b, c, ns):
    outputs = run(a, b, c, ns)
    return ",".join(str(i) for i in outputs)


def p2(a, b, c, ns):
    outputs = run(a, b, c, ns)
    ns = list(ns)
    candidate = 2
    digit_first_seen = {}
    deltas = {}
    while True:
        outputs = run(candidate, b, c, ns, max_outputs=len(ns))
        # keep track of the rough increments required to move each number
        if len(outputs) > len(digit_first_seen):
            digit_first_seen[len(outputs)] = candidate

        if outputs == ns:
            return candidate

        if len(outputs) < len(ns):
            candidate *= 2
        elif len(outputs) > len(ns):
            candidate == candidate // 2
        else:
            if not deltas:
                deltas = digit_first_seen.copy()

            for i in range(len(ns) - 1, -1, -1):
                if outputs[i] == ns[i]:
                    continue

                # Lower the increment based on how close we are to a solution
                delta = digit_first_seen[i - 3] if i > 3 else 1
                candidate += delta

    return None


filename = sys.argv[1] if len(sys.argv) > 1 else "test"
a, b, c, *ns = map(int, re.findall("\d+", open(filename).read().replace("\n", " ")))
print(p1(a, b, c, ns))
print(p2(a, b, c, ns))
