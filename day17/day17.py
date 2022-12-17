import itertools
import advent_tools


ALL_SHAPES = {
    0: {(0, 0), (1, 0), (2, 0), (3, 0)},
    1: {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)},
    2: {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)},
    3: {(0, 0), (0, 1), (0, 2), (0, 3)},
    4: {(0, 0), (1, 0), (0, 1), (1, 1)},
}


def main():
    data = advent_tools.read_whole_input()
    period_info = find_period(data)
    print('Part 1:', get_lines(period_info, 2022))
    print('Part 2:', get_lines(period_info, 1000000000000))


def find_period(data):
    skip_steps = 50
    grid = {(x, 0) for x in range(7)}
    jet_index = -1
    jet_cycle = itertools.cycle(enumerate(data))
    cycle_record = {}
    shape_cycle = itertools.cycle(range(5))
    step = 0
    while True:
        shape_num = next(shape_cycle)
        lines = find_max_y(grid)
        if step > skip_steps:
            profile = get_profile(grid)
            cache_key = (profile, shape_num, jet_index)
            if cache_key in cycle_record:
                old_step, old_lines = cycle_record[cache_key]
                return old_step, old_lines, step, lines, cycle_record
            cycle_record[cache_key] = (step, lines)
        step = step + 1
        cur_x = 2
        cur_y = lines + 4
        shape = ALL_SHAPES[shape_num]
        moved = True
        while moved :
            jet_index, jet = next(jet_cycle)
            if jet == ">":
                cur_x, cur_y, _ = try_move(grid, shape, cur_x, cur_y, 1, 0)
            else:
                cur_x, cur_y, _ = try_move(grid, shape, cur_x, cur_y, -1, 0)
            cur_x, cur_y, moved = try_move(grid, shape, cur_x, cur_y, 0, -1)
        for delta_x, delta_y in shape:
            grid.add((cur_x + delta_x, cur_y + delta_y))


def find_max_y(grid):
    return max(y for _, y in grid)

def try_move(grid, shape, cur_x, cur_y, delta_x, delta_y):
    new_x = cur_x + delta_x
    new_y = cur_y + delta_y
    if can_move(grid, shape, new_x, new_y):
        return new_x, new_y, True
    else:
        return cur_x, cur_y, False


def can_move(grid, shape, new_x, new_y):
    for delta_x, delta_y in shape:
        x = new_x + delta_x
        if x < 0:
            return False
        if x > 6:
            return False
        if (x, new_y + delta_y) in grid:
            return False
    return True


def get_profile(grid):
    maxes = [get_max_in_col(grid, x) for x in range(7)]
    return tuple(x - min(maxes) for x in maxes)


def get_max_in_col(grid, xval):
    return max(y for x,y in grid if x==xval)


def get_lines(period_info, num_steps):
    old_step, old_lines, step, lines, cycle_record = period_info
    step_period = step - old_step
    line_period = lines - old_lines
    remainder = num_steps % step_period
    same_rem_steps, same_rem_lines = [
        (k, v) for k, v in cycle_record.values() if (k % step_period) == remainder
    ][0]
    answer = (num_steps - same_rem_steps) // step_period * line_period + same_rem_lines
    return answer


if __name__ == '__main__':
    main()
