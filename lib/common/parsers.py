from io import TextIOWrapper


def intlist(string: str, delim=None):
    return list(map(int, string.split(delim)))
