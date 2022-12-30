import re

import advent_tools

CUBE_EDGE_LENGTH = 50

WALL = 2

OPEN_TILE = 1

OFF_MAP = 0


def main():
    data = read_input()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def read_input():
    with open(advent_tools.input_filename()) as in_file:
        contents = in_file.read()
    first_part, second_part = contents.split("\n\n")
    char_map = {' ': OFF_MAP, ".": OPEN_TILE, "#": WALL}
    board_map = advent_tools.PlottingGrid.from_lines(first_part.splitlines(), char_map)
    path = []
    for step in re.findall(r"\d+|L|R", second_part):
        try:
            path.append(int(step))
        except ValueError:
            path.append(step)
    return board_map, path


def run_part_1(data):
    ((row, col), facing) = follow_path(data)
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
        case 0:  # > right
            x = x + 1
        case 1:  # v down
            y = y + 1
        case 2:  # < left
            x = x - 1
        case 3:  # ^ up
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


def take_one_part_two_step(board_map, position, facing):
    size_y, size_x = board_map.grid.shape
    y, x = position
    match facing:
        case 0:  # > right
            x = x + 1
        case 1:  # v down
            y = y + 1
        case 2:  # < left
            x = x - 1
        case 3:  # ^ up
            y = y - 1
    if x >= size_x or x < 0 or y >= size_y or y < 0 or board_map[y, x] == OFF_MAP:
        print(position[0], position[1], "=")
        new_position, new_facing = go_around_corner(position, facing)
        print("=", new_position[0], new_position[1])
        return new_position, new_facing
    return (y, x), facing


def go_around_corner(position, facing):
    y, x = position
    col = x // CUBE_EDGE_LENGTH
    row = y // CUBE_EDGE_LENGTH
    if col == 0:  # D or F
        if row == 2:  # D
            if facing == 2:  # left edge of D, goes to A right
                return (3 * CUBE_EDGE_LENGTH - 1 - y, CUBE_EDGE_LENGTH), 0
            if facing == 3:  # top edge of D, goes to C right
                return (x + CUBE_EDGE_LENGTH, CUBE_EDGE_LENGTH), 0
        if row == 3:  # F
            if facing == 0:  # right edge of F, goes to E up
                return (3 * CUBE_EDGE_LENGTH - 1, y - 2 * CUBE_EDGE_LENGTH), 3
            if facing == 1:  # bottom edge of F, goes to B down
                return (0, x + 2 * CUBE_EDGE_LENGTH), 1
            if facing == 2:  # left edge of F, goes to A down
                return (0, y - 2 * CUBE_EDGE_LENGTH), 1
    if col == 1:  # A, C, or E
        if row == 0:  # A
            if facing == 2:  # left edge of A, goes to D right
                return (3 * CUBE_EDGE_LENGTH - 1 - y, 0), 0
            if facing == 3:  # top edge of A, goes to F right
                return (x + 2 * CUBE_EDGE_LENGTH, 0), 0
        if row == 1:  # C
            if facing == 0:  # right edge of C, goes to B up
                return (CUBE_EDGE_LENGTH - 1, y + CUBE_EDGE_LENGTH), 3
            if facing == 2:  # left edge of C, goes to D down
                return (2 * CUBE_EDGE_LENGTH, y - CUBE_EDGE_LENGTH), 1
        if row == 2:  # E
            if facing == 0:  # right edge of E, goes to B left
                return (3 * CUBE_EDGE_LENGTH - 1 - y, 3 * CUBE_EDGE_LENGTH - 1), 2
            if facing == 1:  # bottom edge of E, goes to F left
                return (x + 2 * CUBE_EDGE_LENGTH, CUBE_EDGE_LENGTH - 1), 2
    if col == 2:  # B
        if row == 0:  # B
            if facing == 0:  # right edge of B, goes to E left
                return (3 * CUBE_EDGE_LENGTH - 1 - y, 2 * CUBE_EDGE_LENGTH - 1), 2
            if facing == 1:  # bottom edge of B, goes to C left
                return (x - CUBE_EDGE_LENGTH, 2 * CUBE_EDGE_LENGTH - 1), 2
            if facing == 3:  # top edge of B, goes to F up
                return (4 * CUBE_EDGE_LENGTH - 1, x - 2 * CUBE_EDGE_LENGTH), 3
    raise ValueError(f"Invalid col {col}, row {row}, facing {facing}, y {y}, x {x}")


def run_part_2(data):
    board_map, path = data
    cur_pos, _ = find_next_pos(board_map, (0, 0), 0)
    facing = 0
    for step in path:
        if isinstance(step, int):
            cur_pos, facing = take_n_part_two_steps(cur_pos, facing, step, board_map)
            print(cur_pos[0], cur_pos[1], facing)
        else:
            facing = take_turn(facing, step)
            print(step, facing)
    return 1000 * (cur_pos[0] + 1) + 4 * (cur_pos[1] + 1) + facing


def take_n_part_two_steps(cur_pos, facing, num_steps, board_map):
    for _ in range(num_steps):
        next_pos, new_facing = take_one_part_two_step(board_map, cur_pos, facing)
        next_val = board_map[next_pos]
        if next_val == WALL:
            return cur_pos, facing
        cur_pos = next_pos
        facing = new_facing
    return cur_pos, facing


if __name__ == '__main__':
    main()
