from lib import advent
from io import TextIOWrapper


@advent.parser(9)
def parse(file: TextIOWrapper):
    return [int(b) for b in file.read().strip()]


@advent.solver(9, part=1)
def solve1(diskmap: list[int]):
    fwd = 0
    bck = len(diskmap) - 1
    checksum = 0
    i = 0
    while fwd < bck:
        for _ in range(diskmap[fwd]):
            diskmap[fwd] -= 1
            checksum += i * ((fwd + 1) // 2)
            i += 1
        fwd += 1
        for _ in range(diskmap[fwd]):
            diskmap[bck] -= 1
            checksum += i * ((bck + 1) // 2)
            i += 1
            if diskmap[bck] == 0:
                bck -= 2
        fwd += 1
    for _ in range(diskmap[bck]):
        checksum += i * ((bck + 1) // 2)
        i += 1
    return checksum


@advent.solver(9, part=2)
def solve2(diskmap: list[int]):
    disk = [-1 for _ in range(sum(diskmap))]
    ptr = 0
    padding = False
    id = 0
    data_bounds = []
    for data in diskmap:
        if not padding:
            disk[ptr:ptr+data] = [id]*data
            id += 1
            data_bounds.append((ptr, ptr+data))
        ptr += data
        padding = not padding

    id -= 1
    L = len(disk)
    d = len(data_bounds) - 1
    start = L - 1
    while start > 0:
        start, end = data_bounds[d]
        d -= 1
        slc = disk[start:end]

        pad_start = 0
        while pad_start < start:
            pad_start = disk.index(-1, pad_start)
            if pad_start > start:
                break
            pad_end = pad_start
            while pad_end < L and disk[pad_end] == -1:
                pad_end += 1
            if pad_end >= L:
                break
            if pad_end - pad_start >= len(slc):
                disk[pad_start:pad_start + len(slc)], disk[start:end] = disk[start:end], disk[pad_start:pad_start + len(slc)]
                break
            pad_start += 1
        id -= 1

    return sum(i * d for i, d in enumerate(disk) if d > 0)
