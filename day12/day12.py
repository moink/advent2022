import contextlib

import numpy as np

import advent_tools


def main():
    print('Part 1:', run_part_1())
    print('Part 2:', run_part_2())


def run_part_1():
    start_pos = HillState.start_pos
    return min_steps_from_pos(start_pos)


def run_part_2():
    all_lengths = []
    for start_pos in zip(*np.where(HillState.elev.grid == 0)):
        num_steps = min_steps_from_pos(start_pos)
        if num_steps is not None:
            all_lengths.append(num_steps)
    return min(all_lengths)


def min_steps_from_pos(start_pos):
    start_state = HillState(start_pos)
    return advent_tools.number_of_bfs_steps(start_state)


def read_elevation_map():
    elev_map = {chr(i + 97): i for i in range(26)}
    elev_map["S"] = -1
    elev_map["E"] = 26
    grid = advent_tools.PlottingGrid.from_file(elev_map)
    start_pos = find_where(grid, -1)
    end_pos = find_where(grid, 26)
    grid[start_pos] = 0
    grid[end_pos] = 25
    return grid, end_pos, start_pos


def find_where(data, val):
    xpos, ypos = np.where(data.grid == val)
    return xpos[0], ypos[0]


class HillState(advent_tools.StateForGraphs):

    elev, end_pos, start_pos = read_elevation_map()

    def __init__(self, start_pos):
        self.cur_pos = start_pos

    def __str__(self):
        return str(self.cur_pos)

    def is_final(self):
        return self.cur_pos == self.end_pos

    def possible_next_states(self):
        result = set()
        steps = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for delta_x, delta_y in steps:
            new_pos = (self.cur_pos[0] + delta_x, self.cur_pos[1] + delta_y)
            with contextlib.suppress(IndexError):
                if self.elev[new_pos] - self.elev[self.cur_pos] <=1:
                    result.add(HillState(new_pos))
        return result

if __name__ == '__main__':
    main()
