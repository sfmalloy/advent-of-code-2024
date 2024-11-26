import sys
import importlib
from pathlib import Path
from requests import HTTPError
from dotenv import load_dotenv

from lib.advent import advent, DayNotFoundException, DuplicateKeyError, Result
from lib.api import download
from lib.cmdline import load_arguments
from lib import constants


def main():
    # importing dynamically so "unused" import isn't removed by accident
    importlib.import_module('solutions')
    args = load_arguments()
    if args.day:
        if args.generate_day:
            generate_new_file(args.day)
        if args.download_input:
            res = download(args.day)
        if not args.download_input and not args.generate_day:
            res = advent.run(args.day, args.file, args.num_runs, args.hide)
            print_table([res])
    elif args.run_all:
        res = advent.run_all(args.num_runs, args.hide)
        print_table(res)


def day_num_file(day_num) -> str:
    if day_num < 10:
        return f'0{day_num}'
    return f'{day_num}'


def print_table(outputs: list[Result]):
    part1_lines = [str(out.part1).splitlines() for out in outputs]
    part2_lines = [str(out.part2).splitlines() for out in outputs]
    width1 = max(8, len(max(part1_lines, key=lambda l: len(l[0]))[0]))
    width2 = max(8, len(max(part2_lines, key=lambda l: len(l[0]))[0]))
    day_width = 5
    time_width = 12
    print('╭{}┬{}┬{}┬{}╮'.format('─'*(day_width+2), '─' *
          (width1+2), '─'*(width2+2), '─'*(time_width+2)))

    print('│ {:^{day}} │ {:^{part1}} │ {:^{part2}} │ {:^{time}} │'
          .format('Day #', 'Part 1', 'Part 2', 'Time (ms)',
                  day=day_width, part1=width1, part2=width2, time=time_width))
    print('├{}┼{}┼{}┼{}┤'.format('─'*(day_width+2), '─' *
          (width1+2), '─'*(width2+2), '─'*(time_width+2)))

    for p1, p2, out in zip(part1_lines, part2_lines, outputs):
        if len(p1) < len(p2):
            for l in range(len(p2)//2):
                print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}} │'
                      .format(' ', ' ', p2[l], ' ', day=day_width, part1=width1, part2=width2, time=time_width))
            print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}.3f} │'
                  .format(day_num_file(out.day), p1[0], p2[len(p2)//2], out.time, day=day_width, part1=width1, part2=width2, time=time_width))
            for l in range(1+len(p2)//2, len(p2)):
                print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}} │'
                      .format(' ', ' ', p2[l], ' ', day=day_width, part1=width1, part2=width2, time=time_width))
        else:
            print('│ {:>{day}} │ {:<{part1}} │ {:<{part2}} │ {:>{time}.3f} │'
                  .format(day_num_file(out.day), p1[0], p2[0], out.time, day=day_width, part1=width1, part2=width2, time=time_width))
    
    if len(outputs) > 1:
        print('├{}┴{}┴{}┼{}┤'.format('─'*(day_width+2), '─' *
            (width1+2), '─'*(width2+2), '─'*(time_width+2)))
        print(f'│ {"Total Time":^{day_width+width1+width2+6}} │ {sum([out.time for out in outputs]):>{time_width}.3f} │')
        print(f'╰{"─"*(day_width+width1+width2+8)}┴{"─"*(time_width+2)}╯')
    else:
        print(f'╰{"─"*(day_width+2)}┴{"─"*(width1+2)}┴{"─"*(width2+2)}┴{"─"*(time_width+2)}╯')


def generate_new_file(day_number):
    path = Path('src') / f'd{day_number:0>2}.py'
    if not path.parent.exists():
        path.parent.mkdir()
    if not path.exists():
        with open(path, 'w') as f:
            f.write(constants.solution_template(day_number))


if __name__ == '__main__':
    load_dotenv()
    MIN_MINOR_VERSION = 12
    if sys.version_info.minor < MIN_MINOR_VERSION:
        print(f'Min version Python 3.{MIN_MINOR_VERSION} required')
        exit()
    try:
        main()
    except DayNotFoundException as err:
        print(err)
    except DuplicateKeyError as err:
        print(err)
        print(f'Found duplicate solution key {err.key}')
    except HTTPError as err:
        pass
