import sys
import importlib
from pathlib import Path
from requests import HTTPError
from dotenv import load_dotenv

from lib.advent import advent, DayNotFoundException, DuplicateKeyError, Result
from lib.api import download
from lib.cmdline import load_arguments
from lib.printer import print_table
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
            file = 'test.in' if args.use_test_input else args.file
            res = advent.run(args.day, file, args.num_runs, args.hide, args.part)
            print_table([res])
    elif args.run_all:
        res = advent.run_all(args.num_runs, args.hide)
        print_table(res)


def day_num_file(day_num) -> str:
    if day_num < 10:
        return f'0{day_num}'
    return f'{day_num}'


def generate_new_file(day_number):
    path = Path('solutions') / f'd{day_number:0>2}.py'
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
