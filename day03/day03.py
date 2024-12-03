import re

text = open("input").read()

p1_ops = re.findall(r"mul\((\d+),(\d+)\)", text)
print(sum(int(l) * int(r) for l, r in p1_ops))

p2_ops = re.findall(r"(mul\((\d+),(\d+)\)|do\(\)|don't\(\))", text)
enabled = True
p2_result = 0
for op, l, r in p2_ops:
    if op == "don't()":
        enabled = False
    elif op == "do()":
        enabled = True
    elif enabled:
        p2_result += int(l) * int(r)

print(p2_result)
