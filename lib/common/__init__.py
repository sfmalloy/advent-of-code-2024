'''
Common helper functions and classes used in puzzle solutions
'''
import math

def magnitude(num: int) -> int:
    return int(math.log10(num) + 1)


def intlist(string: str, delim=None) -> list[int]:
    return list(map(int, string.split(delim)))
