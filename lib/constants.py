YEAR = 2024
MONTH = 12
URL = f'https://adventofcode.com/{YEAR}'

def solution_template(day_number: int) -> str:
    return f'''from io import TextIOWrapper
from dataclasses import dataclass
from lib.advent import advent

@advent.parser({day_number})
def parse(file: TextIOWrapper):
    lines = [line.strip() for line in file.readlines()]
    return lines


@advent.day({day_number}, part=1)
def solve1(ipt):
    return 0


@advent.day({day_number}, part=2)
def solve2(ipt):
    return 0
'''
