import abc
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


def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    elves = set()
    for y_pos, line in enumerate(data):
        for x_pos, char in enumerate(line):
            if char == "#":
                elves.add((x_pos, y_pos))
    return elves


class Direction(abc.ABC):

    @abc.abstractmethod
    def places_to_check(self, x, y):
        pass

    @abc.abstractmethod
    def place_to_move(self, x, y):
        pass


class North(Direction):

    def places_to_check(self, x, y):
        return {(x, y - 1), (x - 1, y - 1), (x + 1, y - 1)}

    def place_to_move(self, x, y):
        return x, y - 1


class South(Direction):

    def places_to_check(self, x, y):
        return {(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)}

    def place_to_move(self, x, y):
        return x, y + 1


class East(Direction):

    def places_to_check(self, x, y):
        return {(x + 1, y), (x + 1, y - 1), (x + 1, y + 1)}

    def place_to_move(self, x, y):
        return x + 1, y


class West(Direction):

    def places_to_check(self, x, y):
        return {(x - 1, y), (x - 1, y - 1), (x - 1, y + 1)}

    def place_to_move(self, x, y):
        return x - 1, y


def adjacent_places(x, y):
    cycle = [North(), South(), West(), East()]
    return set.union(*(direction.places_to_check(x, y) for direction in cycle))

def run_part_1(elves):
    # visualize_rectangle(elves)
    cycle = [North(), South(), West(), East()]
    for step in range(10):
        proposal = {}
        for x, y in elves:
            if elves.intersection(adjacent_places(x, y)):
                for direction in cycle:
                    if not elves.intersection(direction.places_to_check(x, y)):
                        proposal[(x, y)] = direction.place_to_move(x, y)
                        break
                    else:
                        proposal[(x, y)] = x, y
            else:
                proposal[(x, y)] = x, y
        elves = set()
        for cur_pos, pro_pos in proposal.items():
            other_prop = {val for key, val in proposal.items() if key != cur_pos}
            if pro_pos in other_prop:
                elves.add(cur_pos)
            else:
                elves.add(pro_pos)
        cycle = [*cycle[1:], cycle[0]]
        # visualize_rectangle(elves)
    max_x, max_y, min_x, min_y = get_rectangle(elves)
    return (max_y - min_y) * (max_x - min_x) - len(elves)


def visualize_rectangle(elves):
    max_x, max_y, min_x, min_y = get_rectangle(elves)
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if (x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print("\n", end="")
    print("")



def get_rectangle(elves):
    all_x = {elf[0] for elf in elves}
    all_y = {elf[1] for elf in elves}
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)
    return max_x + 1, max_y + 1, min_x, min_y


def run_part_2(data):
    pass


if __name__ == '__main__':
    main()
