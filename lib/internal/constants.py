YEAR = 2024
MONTH = 12
URL = f'https://adventofcode.com/{YEAR}'

def solution_template(day_number: int) -> str:
    return f'''from lib import advent
from io import TextIOWrapper
from collections import deque, defaultdict


@advent.parser({day_number})
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return lines


@advent.solver({day_number}, part=1)
def solve1(ipt):
    return 0


@advent.solver({day_number}, part=2)
def solve2(ipt):
    return 0
'''
