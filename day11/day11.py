import contextlib
import collections
import copy
import functools
import itertools
import math
import re
import statistics
import unittest
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

import advent_tools

@dataclass
class Monkey:
    items: collections.deque
    operator: str
    operand: int
    denom: int
    throw_to_true: int
    throw_to_false: int
    divisor: int
    inspection_count: int = 0

    def run_round(self):
        thrown = collections.defaultdict(list)
        while self.items:
            item = self.items.popleft()
            item = self.apply_operation(item)
            item = item // self.divisor
            if item % self.denom == 0:
                thrown[self.throw_to_true].append(item)
            else:
                thrown[self.throw_to_false].append(item)
            self.inspection_count += 1
        return thrown

    def apply_operation(self, item):
        if self.operator == "+":
            return item + self.operand
        if self.operator == "*":
            return item * self.operand
        return item * item

    def append(self, item):
        self.items.append(item)

def main():
    # advent_tools.TESTING = True
    data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    monkeys = process_input(data, 3)
    print('Part 1:', run_part_1(monkeys))
    monkeys = process_input(data, 1)
    # print('Part 2:', run_part_2(monkeys))


def parse_operation(line):
    equation = line.split("=")[1]
    operator = None
    operand = None
    for tentative_operator in ["+", "*"]:
        if tentative_operator in equation:
            operator = tentative_operator
            try:
                operand = int(equation.split(operator)[1])
            except ValueError:
                operator = "^"
                operand = 2
    if operator is None or operand is None:
        raise RuntimeError("Didn't parse operation")
    return operator, operand


def process_input(data , divisor):
    monkeys = {}
    all_denoms = set()
    for line1, line2, line3, line4, line5, line6 in data:
        monkey_num = find_ints(line1)[0]
        items = collections.deque(find_ints(line2))
        operator, operand = parse_operation(line3)
        denom = find_ints(line4)[0]
        throw_to_true = find_ints(line5)[0]
        throw_to_false = find_ints(line6)[0]
        monkeys[monkey_num] = Monkey(
            items, operator, operand, denom, throw_to_true, throw_to_false, divisor
        )
        all_denoms.add(denom)
    print(all_denoms)
    return monkeys

def find_ints(line):
    num_strings = re.findall(r'-?[0-9]+', line)
    nums = [int(num_str) for num_str in num_strings]
    return nums
def run_part_1(monkeys):
    return run_simulation(monkeys, 20)


def run_simulation(monkeys, num_rounds):
    for round_num in range(num_rounds):
        for monkey in monkeys.values():
            thrown = monkey.run_round()
            for to_monkey, items in thrown.items():
                for item in items:
                    monkeys[to_monkey].append(item)
        # print(round_num)
    counts = [monkey.inspection_count for monkey in monkeys.values()]
    return math.prod(sorted(counts, reverse=True)[:2])


def run_part_2(monkeys):
    return run_simulation(monkeys, 10000)
    # 32391000544 is too high

if __name__ == '__main__':
    main()
