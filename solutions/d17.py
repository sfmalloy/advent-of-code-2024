import re
from lib import advent
from io import TextIOWrapper


class Computer:
    registers: list[int]
    ip: list
    prog: list[int]
    halted: bool
    original_state: list[int]

    A = 0
    B = 1
    C = 2

    def __init__(self, a: int, b: int, c: int, program: list[int]):
        self.registers = [a, b, c]
        self.original_state = [a, b, c]
        self.ip = 0
        self.prog = program
        self.halted = False


    def step(self):
        if self.ip < 0 or self.ip >= len(self.prog):
            self.halted = True
            return None
        opcode = self.prog[self.ip]
        output = None
        match opcode:
            case (0 | 6 | 7) as reg: # adv, bdv, cdv
                if reg > 0:
                    reg -= 5
                self.registers[reg] = self.registers[Computer.A] // (2**self.combo_operand())
            case 1: # bxl
                self.registers[Computer.B] ^= self.literal_operand()
            case 2: # bst
                self.registers[Computer.B] = self.combo_operand() % 8
            case 3: # jnz
                if self.registers[Computer.A]:
                    # subtracting 2 because of IP increment at the end
                    self.ip = self.literal_operand() - 2
            case 4: # bxc
                self.registers[Computer.B] = self.registers[Computer.B] ^ self.registers[Computer.C]
            case 5: # out
                output = self.combo_operand() % 8
        self.ip += 2
        return output
    

    def combo_operand(self):
        operand = self.prog[self.ip + 1]
        if 4 <= operand < 7:
            operand = self.registers[operand - 4]
        return operand
    

    def literal_operand(self):
        return self.prog[self.ip + 1]


    def reset(self):
        self.ip = 0
        self.halted = False
        self.registers = [r for r in self.original_state]
    

    def run(self, a=None):
        if a:
            self.registers[Computer.A] = a
        output = []
        while not self.halted:
            if (out := self.step()) is not None:
                output.append(out)
        self.reset()
        return output


@advent.parser(17)
def parse(file: TextIOWrapper):
    registers, program = file.read().split('\n\n')
    a, b, c = map(int, re.findall(r'\d+', registers))
    program = list(map(int, program[len('Program: '):].split(',')))
    return Computer(a, b, c, program)


@advent.solver(17, part=1)
def solve1(comp: Computer):
    return ','.join([str(x) for x in comp.run()])


@advent.solver(17, part=2)
def solve2(comp: Computer):
    a = 0
    for i in range(len(comp.prog)):
        a = find_digit(comp.prog[-(i+1):], comp, a*8)
    return a


def find_digit(goal: list[int], comp: Computer, a: int):
    while True:
        output = comp.run(a)
        if output == goal:
            return a
        a += 1
