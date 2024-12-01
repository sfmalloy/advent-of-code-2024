from lib.internal.runner import Result


class PrintWidths:
    p1: int
    p2: int
    day: int
    time: int

    def __init__(self, p1: bool, p2: bool, multiple: bool):
        self.p1 = 0
        self.p2 = 0
        self.day = 12 if (multiple and not (p1 or p2)) else 7
        self.time = 13


def print_table(outputs: list[Result]):
    p1 = any(out.part1 is not None for out in outputs)
    p2 = any(out.part2 is not None for out in outputs)
    header, widths = _setup(outputs, p1, p2)
    middle = []
    for out in outputs:
        vertical_align = max(out.part1_num_lines, out.part2_num_lines)
        day_lines = [f'{out.day:02d}']
        time_lines = [f'{out.time:.03f}']
        row = ''
        for i in range(vertical_align):
            row += _build_line(i, vertical_align, day_lines, widths.day)
            if p1:
                row += _build_line(i, vertical_align, str(out.part1).splitlines(), widths.p1)
            if p2:
                row += _build_line(i, vertical_align, str(out.part2).splitlines(), widths.p2)
            row += _build_line(i, vertical_align, time_lines, widths.time)
            row += '│\n'
        middle.append(row)
    end = ''
    if len(outputs) > 1:
        end += f'├{'─'*(widths.day)}'
        if p1:
            end += f'┴{'─'*(widths.p1)}'
        if p2:
            end += f'┴{'─'*(widths.p2)}'
        end += f'┼{'─'*(widths.time)}┤\n'
        end += f'│{'Total Time':^{widths.day + widths.p1 + widths.p2 + (2 if p1 or p2 else 0)}}'
        end += f'│{sum([out.time for out in outputs]):>{widths.time-1}.3f} │\n'
        end += f'╰{'─'*(widths.day + widths.p1 + widths.p2 + (2 if p1 or p2 else 0))}┴{'─'*(widths.time)}╯'
    else:
        end += f'╰{'─'*(widths.day)}'
        if p1:
            end += f'┴{"─"*(widths.p1)}'
        if p2:
            end += f'┴{"─"*(widths.p2)}'
        end += f'┴{"─"*(widths.time)}╯'

    print(header, end='')
    print((_build_separator(widths, p1, p2)).join(middle), end='')
    print(end)


def _build_line(i: int, v: int, lines: list[str], width: int):
    start = (v-len(lines)) // 2
    end = start + len(lines)
    if i >= start and i < end:
        return f'│ {lines[i-start]:>{width-2}} '
    return f'│{' ':>{width}}'


def _build_separator(widths: PrintWidths, p1: bool, p2: bool):
    sep = f'├{'─'*(widths.day)}'
    if p1:
        sep += f'┼{'─'*(widths.p1)}'
    if p2:
        sep += f'┼{'─'*(widths.p2)}'
    sep += f'┼{'─'*(widths.time)}┤\n'
    return sep


def _setup(outputs: list[Result], p1: bool, p2: bool) -> tuple[str, PrintWidths]:
    widths = PrintWidths(p1, p2, len(outputs) > 1)
    header = f'╭{'─'*(widths.day)}'
    if p1:
        widths.p1 = max(8, max(out.part1_line_length+2 for out in outputs))
        header += f'┬{'─'*(widths.p1)}'
    if p2:
        widths.p2 = max(8, max(out.part2_line_length+2 for out in outputs))
        header += f'┬{'─'*(widths.p2)}'
    header += f'┬{'─'*(widths.time)}╮\n'

    header += f'│{'Day #':^{widths.day}}'
    if p1:
        header += f'│{'Part 1':^{widths.p1}}'
    if p2:
        header += f'│{'Part 2':^{widths.p2}}'
    header += f'│{'Time (ms)':^{widths.time}}│\n'
    header += _build_separator(widths, p1, p2)
    return header, widths
