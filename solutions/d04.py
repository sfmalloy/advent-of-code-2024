from lib import advent
from io import TextIOWrapper


@advent.parser(4)
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return lines


@advent.solver(4, part=1)
def solve1(lines: list[str]):
    count = search_horiz(lines)
    count += search_horiz(list(''.join(line) for line in zip(*lines)))
    count += search_diag(lines)
    count += search_diag([line[::-1] for line in lines])
    return count


@advent.solver(4, part=2, reparse=False)
def solve2(lines: list[str]):
    count = 0
    VALID = {'MSSM', 'SSMM', 'MMSS', 'SMMS'}
    for i in range(1, len(lines)-1):
        for j in range(1, len(lines[i])-1):
            if lines[i][j] == 'A':
                key = lines[i-1][j-1] + lines[i-1][j+1] + lines[i+1][j+1] + lines[i+1][j-1]
                if key in VALID:
                    count += 1
    return count


def search_horiz(lines: list[str]) -> int:
    count = 0
    for line in lines:
        for j in range(len(line)-3):
            if line[j] in 'XS':
                guess = line[j:j+4]
                if guess == 'XMAS' or guess == 'SAMX':
                    count += 1
    return count


def search_diag(lines: list[str]) -> int:
    count = 0
    for i in range(len(lines)-3):
        for j in range(len(lines[i])-3):
            if lines[i][j] in 'XS':
                guess = lines[i][j] + lines[i+1][j+1] + lines[i+2][j+2] + lines[i+3][j+3]
                if guess == 'XMAS' or guess == 'SAMX':
                    count += 1
    return count
