# Advent of Code 2024

These are my solutions for [Advent of Code 2024](https://adventofcode.com/2024) written in Python 3.12. This repo uses a small [library I mostly wrote in 2023](https://github.com/sfmalloy/advent-of-code-2023/) but has some significant updates this year. The library is used to automate input downloading and solution importing/timing, and includes some common utilities used in writing solutions. It does **not** support answer submission.

## Commands

### Run single day
```
python run.py -d <day_number>
```

### Run all days
```
python run.py -a
```

### All flags
|Flag|Description|
|:-|:-|
|`-h, --help`|Show help message.|
|`-d DAY, --day DAY`|Runs day <d>. If `-f` is not specified, the regular puzzle input is used as input.|
|`-a, --all`|Run all days.|
|`-f FILE, --file FILE`|Specify different input file from default.|
|`-t, --test`|Shorthand for `-f test.in`. Overrides `-f` argument.|
|`-n NUM_RUNS, --numruns NUM_RUNS`|Specify number of runs to get an average time.|
|`-x, --hide`|Hide answers from output table, only showing day number and runtime.|
|`-i, --input`|Download if not cached and print input for the given day.|
|`-g, --generate`|Generate template solution file for the given day.|
|`-p {1,2}, --part {1,2}`|Part number to run. If part 2 depends on part 1, then part 1 is still run but only part 2 is output.|

## Dependencies
The solutions themselves (unless otherwise stated later) rely only on whatever is in the Python standard library at the time. The runner library uses some outside dependencies for downloading input and loading environment variables. To install simply run:
```
pip install -r requirements.txt
```

## Solution Layout
This library can dynamically add solutions (solver functions) without modifying `run.py`. You simply import the global `advent` object (from the local `lib.advent` module), and use a decorator to mark your function as a solver.

Your solver function must accept at least one parameter which either is the file input of type `TextIOWrapper`, OR input parsed in a way that you define in a custom parser function (examples shown below). 

### Without parser function:
```py
from lib.advent import advent
from io import TextIOWrapper


@advent.solver(1)
def solve(file: TextIOWrapper):
    lines = file.readlines()
    # ...do something with the input and set return values
    return part1, part2
```

### With custom parser:
```py
from lib.advent import advent
from io import TextIOWrapper

@advent.parser(1)
def parse(file: TextIOWrapper) -> list[str]:
    return [line.strip() for line in file.readlines()]


@advent.solver(1)
def solve(lines: list[str]):
    lines = file.readlines()
    # ...do something with the input and set return values
    return part1, part2
```

An input parser can also return multiple arguments in a tuple, and be passed as seperate arguments to each solver for that day. For example:
```py
from lib.advent import advent
from io import TextIOWrapper

@advent.parser(1)
def parse(file: TextIOWrapper) -> tuple[str, int]:
    lines = file.readlines()
    a = lines[0]
    b = int(lines[1])
    return a, b


@advent.solver(1)
def solve(a: str, b: int):
    #...
```

Another way to organize your solvers is have seperate functions for parts 1 and 2. All you need to do is declare in the decorator what part each function is solving. **The input is freshly parsed between calls to part 1 and 2 solvers unless otherwise specified** (see [Solution Attributes](#solution-attributes)).

```py
from .lib.advent import advent
from io import TextIOWrapper


# you can choose to optionally write out `part=` if you want for clarity
@advent.solver(1, part=1)
def day1_part1(file: TextIOWrapper):
    lines = file.readlines()
    # ...do something with the input and set part 1 return value
    return part1


@advent.solver(1, 2)
def day1_part2(file: TextIOWrapper):
    lines = file.readlines()
    # ...do something with the input again and set part 2 return value
    return part2
```

## Solver Attributes
Part 2 solvers can have some special attributes as well.

`use_part1: bool (default False)` - used for very specific scenarios when you want to use part 1's answer in the part 2 function.

```py
@advent.solver(1, part=2, use_part1=True)
def solve2(ipt, part1_answer):
    # ...
```

`reparse: bool (default True)` - used to specify whether to run the parser function (if present) again between part 1 and part 2 functions (if both exist). If `False` and the parsed input is modified, those modifications will carry over to part 2 (assuming the input is mutable).

```py
@advent.solver(1, part=2, reparse=False)
def solve2(ipt):
    # ...
```
