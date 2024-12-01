import sys

lines = sys.stdin.read().strip().split("\n")
ll, rl = zip(*[map(int, l.split()) for l in lines])
dists = []
for l, r in zip(sorted(ll), sorted(rl)):
    dists.append(abs(l - r))

print(sum(dists))
similarity_score = 0
for l in ll:
    similarity_score += l * rl.count(l)

print(similarity_score)
