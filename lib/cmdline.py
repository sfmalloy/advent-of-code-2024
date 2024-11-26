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


def load_arguments() -> AdventNamespace:
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('-d', '--day', dest='day', help='Runs day <d>. If -f is not specified, '
                        'the regular puzzle input is used as input.', type=int)
    parser.add_argument('-a', '--all', action='store_true', dest='run_all',
                        default=False, help='Run all days.')
    parser.add_argument('-f', '--file', dest='file',
                        help='Specify different input file from default.')
    parser.add_argument('-n', '--numruns', dest='num_runs',
                        help='Specify number of runs to get an average time.', default=1, type=int)
    parser.add_argument('-x', '--hide', action='store_true', dest='hide',
                        help='Replace answer output with a bunch of X\'s.', default=False)
    parser.add_argument('-i', '--input', action='store_true', dest='download_input',
                        help='Only download/print input for day.', default=False)
    parser.add_argument('-g', '--generate', action='store_true', dest='generate_day',
                        help='Generate template solution file for given day,', default=False)
    parser.add_argument('-t', '--test', action='store_true', dest='use_test_input',
                        help='Shorthand for -f test.in. Overrides -f argument.')

    return parser.parse_args(namespace=AdventNamespace())
