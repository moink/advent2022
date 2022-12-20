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
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    nodes = []
    zero_node = None
    for num in data:
        node = advent_tools.LinkedListNode(num)
        nodes.append(node)
        if num == 0:
            zero_node = node
    num_nodes = len(nodes)
    for i in range(num_nodes - 1):
        nodes[i].next = nodes[i+1]
    for i in range(1, num_nodes):
        nodes[i].previous = nodes[i - 1]
    nodes[num_nodes - 1].next = nodes[0]
    nodes[0].previous = nodes[num_nodes - 1]
    return nodes, zero_node


def print_linked_list(head):
    result = str(head) + ' '
    place = head.next
    while place != head:
        result = result + str(place) + ' '
        place = place.next
    print(result)


def get_nth_node(start_node, num_steps):
    cur_node = start_node
    for _ in range(num_steps):
        cur_node = cur_node.next
    return cur_node.data


def run_part_1(data):
    nodes, zero_node = data
    for node in nodes:
        steps = node.data
        if steps > 0:
            for _ in range(steps):
                move_once_positive(node)
        else:
            for _ in range(-steps):
                move_once_negative(node)
    return sum(get_nth_node(zero_node, 1000 * n) for n in range(1, 4))


def move_once_positive(node):
    arrange_four_nodes(node.previous, node.next, node, node.next.next)

def move_once_negative(node):
    arrange_four_nodes(node.previous.previous, node, node.previous, node.next)

def arrange_four_nodes(first, second, third, fourth):
    re_attach_nodes(first, second)
    re_attach_nodes(second, third)
    re_attach_nodes(third, fourth)


def re_attach_nodes(left, right):
    left.next = right
    right.previous = left



def run_part_2(data):
    pass


if __name__ == '__main__':
    main()
