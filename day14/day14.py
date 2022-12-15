import copy

import numpy as np

import advent_tools


def main():
    data = advent_tools.read_all_integers()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    result = advent_tools.PlottingGrid((800, 800))
    pairs = [list(zip(*[iter(line)]*2)) for line in data]
    for line in pairs:
        for (x1, y1), (x2, y2) in ((line[i], line[i + 1])
                                   for i in range(len(line) - 1)):
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            result.grid[y1:y2 + 1, x1:x2 + 1] = 1
    result.grid, shift = array_trim(result.grid)
    start_point = (0, 500 - shift)
    return result, start_point

def array_trim(arr, margin=0):
    all_y, all_x = np.where(arr != 0)
    min_x = min(all_x) - 150
    max_x = max(all_x) + 150
    max_y = max(all_y) + 2
    return arr[0:max_y +1, min_x: max_x + 1], min_x

def run_part_1(data):
    grid, start_pos = data
    return run_sand_sim(copy.deepcopy(grid), start_pos)


def run_sand_sim(grid, start_pos):
    keep_going = True
    count = -1
    while keep_going:
        cur_y, cur_x = start_pos
        while True:
            new_y = cur_y + 1
            try:
                if grid[new_y, cur_x] == 0:
                    cur_x, cur_y = cur_x, new_y
                elif grid[new_y, cur_x - 1] == 0:
                    cur_x, cur_y = cur_x - 1, new_y
                elif grid[new_y, cur_x + 1] == 0:
                    cur_x, cur_y = cur_x + 1, new_y
                else:
                    grid[cur_y, cur_x] = 2
                    if (cur_y, cur_x) == start_pos:
                        keep_going = False
                    break
            except IndexError:
                keep_going = False
                break
        count = count + 1
    grid.show()
    return count


def run_part_2(data):
    grid, start_pos = data
    grid.grid[-1, :] = 1
    return run_sand_sim(grid, start_pos) + 1


if __name__ == '__main__':
    main()
