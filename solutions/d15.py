from lib import advent
from lib.common.vec import Vec2, RCDir
from io import TextIOWrapper


@advent.parser(15)
def parse(file: TextIOWrapper):
    grid_lines, instruction_lines = file.read().split('\n\n')
    
    grid = []
    start = None
    for r, row in enumerate(grid_lines.splitlines()):
        grid.append(list(row.strip()))
        if (c := row.find('@')) != -1:
            start = Vec2(r, c)
    grid[start.r][start.c] = '.'

    instructions = []
    for ins in ''.join(instruction_lines.splitlines()):
        match ins:
            case '>':
                instructions.append(RCDir.R)
            case '<':
                instructions.append(RCDir.L)
            case '^':
                instructions.append(RCDir.U)
            case 'v':
                instructions.append(RCDir.D)
    return grid, instructions, start


@advent.solver(15, part=1)
def solve1(grid: list[list[str]], instructions: list[Vec2], pos: Vec2):

    def push_box(direction: Vec2, pos: Vec2):
        if grid[pos.r][pos.c] == '.':
            grid[pos.r][pos.c] = 'O'
            return True
        elif grid[pos.r][pos.c] == '#':
            return False
        return push_box(direction, pos + direction)


    for dir in instructions:
        new = (pos+dir)
        sym = grid[new.r][new.c]
        if sym == 'O':
            if push_box(dir, pos+dir):
                pos = new
                grid[pos.r][pos.c] = '.'
        elif sym == '.':
            pos = new
    
    ans = 0
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == 'O':
                ans += 100 * r + c
    return ans


@advent.solver(15, part=2)
def solve2(grid: list[list[str]], instructions: list[Vec2], pos: Vec2):
    
    def check_box_vertical(direction: Vec2, pos: Vec2, visited: set):
        if pos in visited:
            return True
        visited.add(pos)
        if grid[pos.r][pos.c] == '.':
            return True
        elif grid[pos.r][pos.c] == '#':
            return False
        
        neighbor = RCDir.R if grid[pos.r][pos.c] == '[' else RCDir.L
        return check_box_vertical(direction, pos + direction, visited) and check_box_vertical(direction, pos + neighbor, visited)


    def push_box_vertical(dir: Vec2, pos: Vec2, visited: set):
        if pos in visited:
            return
        visited.add(pos)
        if grid[pos.r][pos.c] == '[':
            new = pos + dir
            push_box_vertical(dir, new, visited)
            push_box_vertical(dir, pos + RCDir.R, visited)

            grid[pos.r][pos.c] = '.'
            grid[new.r][new.c] = '['
        elif grid[pos.r][pos.c] == ']':
            new = pos + dir
            push_box_vertical(dir, new, visited)
            push_box_vertical(dir, pos + RCDir.L, visited)

            grid[pos.r][pos.c] = '.'
            grid[new.r][new.c] = ']'


    def push_box_horizontal(grid: list[list[str]], direction: Vec2, pos: Vec2):
        if grid[pos.r][pos.c] == '.':
            old = pos - dir
            grid[pos.r][pos.c] = grid[old.r][old.c]
            return pos
        elif grid[pos.r][pos.c] == '#':
            return None

        end = push_box_horizontal(grid, direction, pos + direction)
        if end:
            old = pos-dir
            grid[pos.r][pos.c] = grid[old.r][old.c]
        return end
    
    new_grid = []
    for row in grid:
        new_row = []
        for col in row:
            match col:
                case '#':
                    new_row.append('#')
                    new_row.append('#')
                case '.':
                    new_row.append('.')
                    new_row.append('.')
                case 'O':
                    new_row.append('[')
                    new_row.append(']')
        new_grid.append(new_row)
    grid = new_grid
    pos = Vec2(pos.r, pos.c*2)

    for dir in instructions:
        new = pos + dir
        sym = grid[new.r][new.c]
        if sym == '[' or sym == ']':
            if (dir == RCDir.U or dir == RCDir.D) and check_box_vertical(dir, new, set()):
                push_box_vertical(dir, new, set())
                pos = new
            elif (dir == RCDir.R or dir == RCDir.L) and push_box_horizontal(grid, dir, new):
                pos = new
        elif sym == '.':
            pos = new

    ans = 0
    for r, row in enumerate(grid):
        for c, col in enumerate(row):
            if col == '[':
                ans += 100 * r + c
    return ans
