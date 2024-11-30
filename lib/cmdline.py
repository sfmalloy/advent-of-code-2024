from argparse import ArgumentParser, Namespace


class AdventNamespace(Namespace):
    day: int
    run_all: bool
    file: str
    num_runs: int
    hide: bool
    download_input: bool
    generate_day: bool
    use_test_input: bool
    part: int


def load_arguments() -> AdventNamespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-d', '--day', dest='day', type=int,
                        help='Runs day <d>. If -f is not specified, the regular puzzle input is used as input.')
    parser.add_argument('-a', '--all', action='store_true', dest='run_all', default=False,
                        help='Run all days.')
    parser.add_argument('-f', '--file', dest='file',
                        help='Specify different input file from default.')
    parser.add_argument('-t', '--test', action='store_true', dest='use_test_input',
                        help='Shorthand for -f test.in. Overrides -f argument.')
    parser.add_argument('-n', '--numruns', dest='num_runs', default=1, type=int,
                        help='Specify number of runs to get an average time.')
    parser.add_argument('-x', '--hide', action='store_true', dest='hide', default=False,
                        help='Hide answers from output table, only showing day number and runtime.')
    parser.add_argument('-i', '--input', action='store_true', dest='download_input', default=False,
                        help='Download if not cached and print input for the given day.')
    parser.add_argument('-g', '--generate', action='store_true', dest='generate_day', default=False,
                        help='Generate template solution file for the given day.')
    parser.add_argument('-p', '--part', dest='part', type=int, choices=[1, 2],
                        help='Part number to run. If part 2 depends on part 1, then part 1 is still run but only part 2 is output.')

    return parser.parse_args(namespace=AdventNamespace())
