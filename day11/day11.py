import collections
import math
import re
from dataclasses import dataclass

import advent_tools


def main():
    data = advent_tools.read_input_line_groups()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    monkeys = process_input(data, Monkey)
    return run_simulation(monkeys, 20)


def process_input(data, monkey_class):
    monkeys = {}
    for lines in data:
        monkey_num = find_ints(lines[0])[0]
        items = collections.deque(find_ints(lines[1]))
        operator, operand = parse_operation(lines[2])
        denom = find_ints(lines[3])[0]
        throw_to_true = find_ints(lines[4])[0]
        throw_to_false = find_ints(lines[5])[0]
        monkeys[monkey_num] = monkey_class(
            items, operator, operand, denom, throw_to_true, throw_to_false
        )
    return monkeys


def find_ints(line):
    num_strings = re.findall(r'-?[0-9]+', line)
    nums = [int(num_str) for num_str in num_strings]
    return nums


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


def run_simulation(monkeys, num_rounds):
    for round_num in range(num_rounds):
        for monkey in monkeys.values():
            thrown = monkey.run_round()
            for to_monkey, items in thrown.items():
                for item in items:
                    monkeys[to_monkey].append(item)
    counts = [monkey.inspection_count for monkey in monkeys.values()]
    return math.prod(sorted(counts, reverse=True)[:2])


def run_part_2(data):
    monkeys = process_input(data, MonkeyPartTwo)
    all_denoms = {monkey.denom for monkey in monkeys.values()}
    for monkey in monkeys.values():
        monkey.break_up_items(all_denoms)
    return run_simulation(monkeys, 10000)


@dataclass
class Monkey:
    items: collections.deque
    operator: str
    operand: int
    denom: int
    throw_to_true: int
    throw_to_false: int

    inspection_count: int = 0

    def run_round(self):
        thrown = collections.defaultdict(list)
        while self.items:
            item = self.items.popleft()
            item = self.apply_operation(item)
            if self.get_modulus(item) == 0:
                thrown[self.throw_to_true].append(item)
            else:
                thrown[self.throw_to_false].append(item)
            self.inspection_count += 1
        return thrown

    def append(self, item):
        self.items.append(item)

    def apply_operation(self, item):
        if self.operator == "+":
            return (item + self.operand) // 3
        if self.operator == "*":
            return (item * self.operand) // 3
        return (item * item) // 3

    def get_modulus(self, item):
        return item % self.denom


class MonkeyPartTwo(Monkey):

    def apply_operation(self, item):
        if self.operator == "+":
            return {key: (val + self.operand) % key for key, val in item.items()}
        if self.operator == "*":
            return {key: (val * self.operand) % key for key, val in item.items()}
        return {key: (val * val) % key for key, val in item.items()}

    def get_modulus(self, item):
        return item[self.denom]

    def break_up_items(self, all_denoms):
        self.items = collections.deque([
            {denom: item % denom for denom in all_denoms}
            for item in self.items
        ])


if __name__ == '__main__':
    main()
