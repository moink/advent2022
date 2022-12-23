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

WALL = 2

OPEN_TILE = 1

OFF_MAP = 0


def main():
    # advent_tools.TESTING = True
    # data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    data = read_input()
    # data = advent_tools.read_nparray_from_digits()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def read_input():
    with open(advent_tools.input_filename()) as in_file:
        contents = in_file.read()
    first_part, second_part = contents.split("\n\n")
    char_map ={' ': OFF_MAP, ".": OPEN_TILE, "#": WALL}
    board_map = advent_tools.PlottingGrid.from_lines(first_part.splitlines(), char_map)
    path = []
    for step in re.findall(r"\d+|L|R", second_part):
        try:
            path.append(int(step))
        except ValueError:
            path.append(step)
    print(path)
    return board_map, path


def run_part_1(data):
    ((row, col), facing) = follow_path(data)
    # print(facing)
    # 11428 is too low
    return 1000 * row + 4 * col + facing

def follow_path(data):
    board_map, path = data
    cur_pos, _ = find_next_pos(board_map, (0, 0), 0)
    facing = 0
    for step in path:
        if isinstance(step, int):
            cur_pos = take_up_to_n_steps(cur_pos, facing, step, board_map)
        else:
            facing = take_turn(facing, step)
    return tuple(n + 1 for n in cur_pos), facing


def take_turn(facing, turn):
    if turn == "R":
        delta = 1
    else:
        delta = -1
    return (facing + delta) % 4


def take_up_to_n_steps(cur_pos, facing, num_steps, board_map):
    for _ in range(num_steps):
        next_pos, next_val = find_next_pos(board_map, cur_pos, facing)
        if next_val == WALL:
            return cur_pos
        cur_pos = next_pos
    return cur_pos


def find_next_pos(board_map, position, facing):
    next_val = OFF_MAP
    next_spot = position
    while next_val == OFF_MAP:
        next_spot = take_one_step(next_spot, facing, board_map.grid.shape)
        next_val = board_map[next_spot]
    return next_spot, next_val


def take_one_step(position, facing, shape):
    size_y, size_x = shape
    y, x = position
    match facing:
        case 0: # > right
            x = x + 1
        case 1: # v down
            y = y + 1
        case 2: # < left
            x = x - 1
        case 3: # ^ up
            y = y - 1
    x = check_edges(x, size_x)
    y = check_edges(y, size_y)
    return y, x


def check_edges(x, size_x):
    if x >= size_x:
        x = 0
    if x < 0:
        x = size_x - 1
    return x


def run_part_2(data):
    pass


if __name__ == '__main__':
    main()
