# Advent of Code 2024

These are my solutions for [Advent of Code 2024](https://adventofcode.com/2024)! They are written in Python 3 using CPython 3.12. This uses a small runner library I [mostly wrote in 2023](https://github.com/sfmalloy/advent-of-code-2023/) that automatically downloads and caches input and can do things like run from test input files. The only thing it does not do is submit answers. You can run either a single day to get its answer and runtime, or run all the available days and get their combined runtime.

## Commands

### Run single day
```
python run.py -d <day_number>
```

### Run all days
```
python run.py -a
```

### Other flags
```
-h, --help                          Show help message.
-f <filepath>, --file <filepath>    Specify different input file from default.
-t, --test                          Shorthand for -f test.in. Overrides -f argument.
-n <number>, --numruns <number>     Specify number of runs to get an average time.
-x, --hide                          Replace answer output with a bunch of X's.
-i, --input                         Download/print input for day and do not run the solution.
-g, --generate                      Generate template solution file for given day.
```

## Dependencies
The solutions themselves (unless otherwise stated later) rely only on whatever is in the Python standard library at the time. The runner library uses some outside dependencies for downloading input and loading environment variables. To install simply run:
```
pip install -r requirements.txt
```

## Solution Layout
This library can dynamically add solutions without modifying `run.py`. Instead, you simply import a global `advent` object (from the local `lib.advent` module), and use a decorator to mark your function as a solution.

Your solution function must accept 1 parameter which either is the file input of type `TextIOWrapper`, OR input parsed in a way that you define in a custom parser function (examples shown below). 

### Without parser function:
```py
from lib.advent import advent
from io import TextIOWrapper


@advent.day(1)
def day1(file: TextIOWrapper):
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


@advent.day(1)
def day1(lines: list[str]):
    lines = file.readlines()
    # ...do something with the input and set return values
    return part1, part2

```

Another way to organize your solvers is have seperate functions for parts 1 and 2. All you need to do is declare in the decorator what part each function is solving. **The input is freshly parsed between calls to part 1 and 2 functions unless otherwise specified** (see [Solution Attributes](#solution-attributes)).

```py
from .lib.advent import advent
from io import TextIOWrapper


# you can choose to optionally write out `part=` if you want for clarity
@advent.day(1, part=1)
def day1_part1(file: TextIOWrapper):
    lines = file.readlines()
    # ...do something with the input and set part 1 return value
    return part1


@advent.day(1, 2)
def day1_part2(file: TextIOWrapper):
    lines = file.readlines()
    # ...do something with the input again and set part 2 return value
    return part2
```

## Solution Attributes
Part 2 functions can have some special attributes as well.

`use_part1: bool (default False)` - used for very specific scenarios when you want to use part 1's answer in the part 2 function.

```py
@advent.day(1, part=2, use_part1=True)
def solve2(ipt, part1_answer):
    # ...
```

`reparse: bool (default True)` - used to specify whether to run the parser function (if present) again between part 1 and part 2 functions (if both exist). If `False` and the parsed input is modified, those modifications will carry over to part 2 (assuming the input is mutable).

```py
@advent.day(1, part=2, reparse=False)
def solve2(ipt):
    # ...
```
