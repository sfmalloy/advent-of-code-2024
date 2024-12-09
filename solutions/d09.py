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
    for data in diskmap:
        if not padding:
            for _ in range(data):
                disk[ptr] = id
                ptr += 1
            id += 1
        else:
            ptr += data
        padding = not padding
    
    id -= 1
    start = len(disk) - 1
    while start > 0:
        # eat padding
        while disk[start] != id:
            start -= 1
        
        # get slice
        end = start + 1
        while disk[start] == id:
            start -= 1
        start += 1
        slc = disk[start:end]

        # find padding
        pad_start = 0
        while pad_start < start:
            while disk[pad_start] != -1:
                pad_start += 1
            if pad_start > start:
                break
            pad_end = pad_start
            while pad_end < len(disk) and disk[pad_end] == -1:
                pad_end += 1
            if pad_end >= len(disk):
                break
            if pad_end - pad_start >= len(slc):
                disk[pad_start:pad_start + len(slc)], disk[start:end] = disk[start:end], disk[pad_start:pad_start + len(slc)]
                break
            pad_start += 1

        id -= 1

    checksum = 0
    for i, d in enumerate(disk):
        if d != -1:
            checksum += i * d
    return checksum
