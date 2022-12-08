import contextlib

import numpy as np

import advent_tools


def main():
    trees = advent_tools.read_nparray_from_digits()
    print('Part 1:', run_part_1(trees))
    print('Part 2:', run_part_2(trees))


def run_part_1(trees):
    return calculate_visibility(trees).sum().sum()


def calculate_visibility(trees):
    cols, rows = trees.shape
    visibility = np.zeros_like(trees, dtype=bool)
    for i in range(rows):
        for j in range(cols):
            this_height = trees[i][j]
            visibility[i, j] = (
                (trees[:i, j] < this_height).all()
                or (trees[i+1:, j] < this_height).all()
                or (trees[i, :j] < this_height).all()
                or (trees[i, j+1:] < this_height).all()
            )
    return visibility


def run_part_2(trees):
    return calculate_scenic_score(trees).max().max()


def calculate_scenic_score(trees):
    cols, rows = trees.shape
    score = np.zeros_like(trees)
    for i in range(rows):
        for j in range(cols):
            score[i, j] = (
                get_treeline_visibility(np.flip(trees[:i+1, j]))
                * get_treeline_visibility(trees[i:, j])
                * get_treeline_visibility(np.flip(trees[i, :j+1]))
                * get_treeline_visibility(trees[i, j:])
            )
    return score


def get_treeline_visibility(tree_line):
    visibility = np.logical_and.accumulate(
        (tree_line < np.maximum.accumulate(tree_line))[1:]
    )
    with contextlib.suppress(IndexError):
        visibility[np.where(~visibility)[0][0]] = True
    return visibility.sum()


if __name__ == '__main__':
    main()
