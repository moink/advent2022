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

# advent_tools.TESTING = True


def main():
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    # data = process_input(data)
    print('Part 1:', run_part_1())
    print('Part 2:', run_part_2())


def process_input(data):
    result = {}
    for line in data:
        line = line.replace("valve ", "valves")
        left, right = line.split("valves")
        destinations = [dest.strip() for dest in right.split(",")]
        _, room, _, _, rest = left.split(" ", maxsplit=4)
        rate = rest.split("=")[1].split(";")[0]
        result[room] = (int(rate), destinations)
    print(result)
    return result

class ParetoSet(set):

    def add(self, element):
        add_it = True
        steps, score = element
        for other_steps, other_score in self:
            if other_steps <= steps and other_score >= score:
                add_it = False
        if add_it:
            super().add(element)
        return add_it

def run_part_1():
    score = get_max_score(ValveState, 30)
    return score


def get_max_score(state_class, max_steps):
    current_state = state_class("AA", set())
    queue = collections.deque()
    discovered = collections.defaultdict(ParetoSet)
    discovered[current_state].add((0, 0))
    queue.append(current_state)
    while queue:
        state = queue.popleft()
        new_states = state.possible_next_states()
        for new_state, delta_flow in new_states:
            for num_steps, score in discovered[state]:
                delta_score = (max_steps - num_steps - 1) * delta_flow
                if num_steps < max_steps:
                    if discovered[new_state].add((num_steps + 1, score + delta_score)):
                        queue.append(new_state)
    score = max(score for state_score in discovered.values() for _, score in state_score)
    return score


class ValveState(advent_tools.StateForGraphs):

    maze = process_input(advent_tools.read_input_lines())

    def __init__(self, pos, opened_valves):
        self.pos = pos
        self.opened_valves = opened_valves

    def __str__(self):
        return '"' + "_".join([self.pos, "-".join(sorted(self.opened_valves))]) + '"'

    def is_final(self):
        return False

    def possible_next_states(self):
        result = {
            (ValveState(new_pos, self.opened_valves), 0) for new_pos in self.maze[self.pos][1]
            if new_pos not in {v for v, _ in self.opened_valves}
        }
        delta_flow = self.maze[self.pos][0]
        if self.pos not in self.opened_valves and delta_flow > 0:
            result.add((ValveState(self.pos, self.opened_valves.union({self.pos})), delta_flow))
        return result


def run_part_2():
    score = get_max_score(ValveState, 26)
    return score


if __name__ == '__main__':
    main()
