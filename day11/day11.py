from functools import lru_cache


@lru_cache(1 << 16)
def stone_count(stone: int, blinks: int) -> int:
    if blinks == 0:
        return 1

    if stone == 0:
        return stone_count(1, blinks - 1)

    if len(str(stone)) % 2 == 0:
        s = str(stone)
        left = int(s[: len(s) // 2])
        right = int(s[len(s) // 2 :])
        return stone_count(left, blinks - 1) + stone_count(right, blinks - 1)

    return stone_count(stone * 2024, blinks - 1)


def solve(stones: list[int], blinks: int) -> int:
    return sum(stone_count(s, blinks) for s in stones)


def p1(stones: list[int]):
    return solve(stones, 25)


def p2(stones: list[int]):
    return solve(stones, 75)


stones = list(map(int, open("input").read().split()))
print(p1(stones))
print(p2(stones))
