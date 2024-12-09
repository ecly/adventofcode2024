import copy
from collections import deque
from dataclasses import dataclass


@dataclass
class FreeSpace:
    idx: int  # probably irrelevant
    size: int


@dataclass
class File:
    idx: int
    size: int


DiskMap = list[File | FreeSpace]


def disk_map_to_result(disk_map: DiskMap) -> list[int | None]:
    result = []
    for f in disk_map:
        idx = None if isinstance(f, FreeSpace) else f.idx
        result.extend([idx] * f.size)
    return result


def pprint(result):
    if isinstance(result[0], File | FreeSpace):
        result = disk_map_to_result(result)
    print("".join(str(i) if i is not None else "." for i in result))


def checksum(result: list[int] | list[int | None]) -> int:
    return sum(pos * idx for pos, idx in enumerate(result) if idx is not None)


def p1(disk_map: DiskMap):
    disk_map = copy.deepcopy(disk_map)
    queue = deque(disk_map)
    result: list[int] = []
    while queue:
        f = queue.popleft()
        if isinstance(f, File):
            for _ in range(f.size):
                result.append(f.idx)
            continue

        free_space = f.size # consume files from the end until space is filled
        while free_space and queue:
            nf = queue.pop()
            if isinstance(nf, FreeSpace):
                continue
            for _ in range(min(free_space, nf.size)):
                result.append(nf.idx)

            if nf.size > free_space:
                nf.size = nf.size - free_space
                free_space = 0
                queue.append(nf)
            else:
                free_space -= nf.size
                nf.size = 0

        # if we didn't consume all of the last file, we just add the remaining.
        # should only happen for the very last file.
        if free_space:
            result.extend([nf.idx] * min(free_space, nf.size))

    return checksum(result)


def p2(disk_map: DiskMap) -> int:
    disk_map = copy.deepcopy(disk_map)
    files = sorted(
        [f for f in disk_map if isinstance(f, File)], key=lambda f: f.idx, reverse=True
    )
    for file in files:
        for i in range(len(disk_map)):
            if i >= len(disk_map):
                break
            fs = disk_map[i]
            if isinstance(fs, File):
                # only allowed to insert to the left of the file
                if fs == file:
                    break

                continue

            if fs.size >= file.size:
                disk_map.pop(i)
                disk_map.insert(i, file)
                if fs.size > file.size:
                    disk_map.insert(i + 1, FreeSpace(fs.idx, fs.size - file.size))

                # replace the last reference (the one we moved) of file
                # with a free space, the size of the file
                for j in range(len(disk_map)):
                    if disk_map[-j] == file:
                        disk_map[-j] = FreeSpace(idx=file.idx, size=file.size)
                        break

                break

    return checksum(disk_map_to_result(disk_map))


disk_map_str = open("input").read().strip()

disk_map: DiskMap = []
for idx, (file_size, free_space) in enumerate(
    zip(disk_map_str[::2], disk_map_str[1::2] + "0")
):
    disk_map.append(File(int(idx), int(file_size)))
    disk_map.append(FreeSpace(int(idx), int(free_space)))

print(p1(disk_map))
print(p2(disk_map))
