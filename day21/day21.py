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
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    data = advent_tools.read_dict_from_input_file(sep=': ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def evaluate_expression(data, monkey_name):
    expression = data[monkey_name]
    try:
        number = int(expression)
    except ValueError:
        pass
    else:
        return number
    left_name, operator, right_name = expression.split()
    left = evaluate_expression(data, left_name)
    right = evaluate_expression(data, right_name)
    match operator:
        case "+":
            return left + right
        case "-":
            return left - right
        case "*":
            return left * right
        case "/":
            return left // right
        case other:
            raise ValueError(f"Unknown operator '{operator}")


def run_part_1(data):
    return evaluate_expression(data, "root")


def run_part_2(data):
    pass


if __name__ == '__main__':
    main()
