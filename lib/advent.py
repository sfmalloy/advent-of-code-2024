from dataclasses import dataclass, field
from io import TextIOWrapper
from pathlib import Path
from timeit import default_timer as timer
from typing import Callable, Any, Optional

from lib.api import download


class DayNotFoundException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DuplicateKeyError(Exception):
    key: str
    def __init__(self, key, *args) -> None:
        super().__init__(args)
        self.key = key


@dataclass
class Result:
    day: int
    time: float = 0
    hide: bool = False
    _part1: Optional[Any] = field(default=None, init=False)
    _part2: Optional[Any] = field(default=None, init=False)

    @property
    def part1(self) -> Any:
        if self.hide and self._part1:
            return None
        return self._part1
    
    @property
    def part2(self) -> Any:
        if self.hide and self._part2:
            return None
        return self._part2
    
    @part1.setter
    def part1(self, v):
        self._part1 = v

    @part2.setter
    def part2(self, v):
        self._part2 = v
    
    @property
    def part1_line_length(self):
        return self._line_length(self.part1)

    @property
    def part2_line_length(self):
        return self._line_length(self.part2)

    @property
    def part1_num_lines(self):
        return self._num_lines(self.part1)

    @property
    def part2_num_lines(self):
        return self._num_lines(self.part2)
    
    def _line_length(self, part: Any) -> int:
        if not part:
            return 4
        l = 0
        for line in str(part).splitlines():
            l = max(l, len(line.strip()))
        return l

    def _num_lines(self, part: Any) -> int:
        if not self.part1:
            return 1
        return len(str(part).splitlines())


@dataclass
class Attribute:
    use_part1: bool=False
    reparse: bool=True


class Advent:
    _days: dict[int | tuple[int, int], Callable[[TextIOWrapper | Any], tuple[Any, Any]]]
    _parsers: dict[int, Callable[[TextIOWrapper], Any]]
    _attrs: dict[int, Attribute]

    def __init__(self):
        self._days = {}
        self._parsers = {}
        self._attrs = {}


    def solver(self, day_number: int, part: int=0, use_part1: bool=False, reparse: bool=True):
        if day_number in self._days:
            raise DuplicateKeyError(day_number)
        elif (day_number, part) in self._days:
            raise DuplicateKeyError((day_number, part))
        '''
        Decorator for a function that is a problem solution.
        '''
        def solver_decorator(fn: Callable):
            self._attrs[day_number] = Attribute(
                use_part1=use_part1,
                reparse=reparse
            )
            if part:
                self._days[(day_number, part)] = fn
            else:
                self._days[day_number] = fn

        return solver_decorator

    def parser(self, day_number: int):
        '''
        Decorator for a function that parses this day's input.
        '''
        def parser_decorator(fn: Callable):
            self._parsers[day_number] = fn

        return parser_decorator


    def run(self, day_number: int, input_path: str=None, num_runs: int=1, hide: bool=False, part: Optional[int]=None):
        if day_number not in self._days \
            and (day_number, 1) not in self._days \
            and (day_number, 2) not in self._days:
            raise DayNotFoundException(f'Day {day_number} solution not found')

        if num_runs == 1:
            return self._run_single(day_number, input_path, hide, part)
        return self._run_multi(day_number, input_path, num_runs, hide, part)


    def run_all(self, num_runs: int=1, hide: bool=False):
        days = set()
        for d in self._days.keys():
            if isinstance(d, tuple):
                days.add(d[0])
            else:
                days.add(d)
        results = []
        for d in days:
            results.append(self.run(d, num_runs=num_runs, hide=hide))
        return results


    def _run_single(self, day_number: int, input_path: str, hide: bool, part: Optional[int]) -> Result:
        path = Path(input_path) if input_path else Path('inputs') / f'd{day_number:0>2}.in'
        if not path.exists():
            download(day_number)

        res = Result(day_number, hide=hide)
        with open(path) as f:
            if day_number not in self._days:
                start_time = timer()
                ipt = f
                if (day_number, 1) in self._days and part != 2:
                    if day_number in self._parsers:
                        ipt = self._parsers[day_number](f)
                    res.part1 = self._call_runner_fn(self._days[(day_number, 1)], ipt)
                if (day_number, 2) in self._days and part != 1:
                    if self._attrs[day_number].reparse or part == 2:
                        f.seek(0, 0)
                        if day_number in self._parsers:
                            ipt = self._parsers[day_number](f)
                    if self._attrs[day_number].use_part1:
                        if not res.part1:
                            res.part1 = self._call_runner_fn(self._days[(day_number, 1)], ipt)
                        res.part2 = self._call_runner_fn(self._days[(day_number, 2)], ipt, res.part1)
                    else:
                        res.part2 = self._call_runner_fn(self._days[(day_number, 2)], ipt)
                end_time = timer()
            else:
                start_time = timer()
                ipt = f
                if day_number in self._parsers:
                    ipt = self._parsers[day_number](f)
                ans = self._call_runner_fn(self._days[day_number], ipt)
                end_time = timer()
                if isinstance(ans, tuple):
                    if part != 2:
                        res.part1 = ans[0]
                    if part != 1:
                        res.part2 = ans[1]
                elif ans:
                    res.part1 = ans

        res.time = 1000 * (end_time - start_time)
        return res
    
    
    def _call_runner_fn(self, fn: Callable, ipt: Any, part1: Optional[Any]=None):
        if part1:
            if isinstance(ipt, tuple):
                return fn(*ipt, part1)
            return fn(ipt, part1)
        if isinstance(ipt, tuple):
            return fn(*ipt)
        return fn(ipt)


    def _run_multi(self, day_number: int, input_path: str, num_runs: int, hide: bool, part: Optional[int]) -> Result:
        time = 0
        latest = None
        for _ in range(num_runs):
            latest = self._run_single(day_number, input_path, hide, part) 
            time += latest.time
        return Result(day_number, time / num_runs, hide, latest.part1, latest.part2)
    

advent = Advent()
