import collections
import functools
import itertools
import math

import advent_tools


def main():
    data = advent_tools.read_input_lines()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(lines):
    blizzards = collections.defaultdict(list)
    for y_pos, line in enumerate(lines[1:-1]):
        for x_pos, char in enumerate(line[1:-1]):
            if char != ".":
                blizzards[char].append((x_pos, y_pos))
    y_size = len(lines) - 2
    x_size = len(lines[0]) - 2
    return blizzards, (x_size, y_size)


def run_part_1(data):
    blizzards, size = data
    return steps_to_navigate_blizzard_maze(
        blizzards, size, (0, - 1), (size[0] - 1, size[1]), 1
    )


def steps_to_navigate_blizzard_maze(blizzards, size, start_pos, goal_state, count):
    cycle_length = math.prod(size)

    @functools.cache
    def empty_spaces_at_step(steps):
        return find_empty_spaces(calculate_blizzards_at_step(blizzards, steps, size), size)

    queue = collections.deque()
    cur_state = (start_pos, count)
    discovered = {cur_state: count}
    queue.append(cur_state)

    while queue:
        state = queue.popleft()
        position = state[0]
        num_steps = discovered[state]
        mod_steps = (num_steps + 1) % cycle_length
        empty_spaces = empty_spaces_at_step(mod_steps)
        for delta_x, delta_y in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            new_x = position[0] + delta_x
            new_y = position[1] + delta_y
            new_pos = (new_x, new_y)
            if new_pos == goal_state:
                return num_steps + 1
            if (new_pos in empty_spaces) or (new_pos == start_pos):
                new_state = new_pos, mod_steps
                if new_state not in discovered:
                    discovered[new_state] = num_steps + 1
                    queue.append(new_state)
    return discovered


def find_empty_spaces(blizzards, size):
    return set(
        itertools.product(range(size[0]), range(size[1]))).difference(
        set.union(*(set(val) for val in blizzards.values()))
    )


def calculate_blizzards_at_step(blizzards, steps, size):
    x_size, y_size = size
    return {
        ">": {((x + steps) % x_size, y) for x, y in blizzards[">"]},
        "<": {((x - steps) % x_size, y) for x, y in blizzards["<"]},
        "v": {(x, (y + steps) % y_size) for x, y in blizzards["v"]},
        "^": {(x, (y - steps) % y_size) for x, y in blizzards["^"]}
    }


def run_part_2(data):
    blizzards, size = data
    start_pos = (0, -1)
    end_pos = size[0] - 1, size[1]
    way_there = steps_to_navigate_blizzard_maze(
        blizzards, size, start_pos, end_pos, 1
    )
    way_back = steps_to_navigate_blizzard_maze(
        blizzards, size, end_pos, start_pos, way_there
    )
    return steps_to_navigate_blizzard_maze(
        blizzards, size, start_pos, end_pos, way_back
    )


def visualize_blizzards(blizzards, size):
    x_size, y_size = size
    print("#.", end="")
    print("#" * x_size)
    for y in range(y_size):
        print("#", end="")
        for x in range(x_size):
            for char, positions in blizzards.items():
                if (x, y) in positions:
                    print(char, end="")
                    break
            else:
                print(".", end="")
        print("#\n", end="")
    print("#" * x_size, end="")
    print(".#\n\n", end="")


if __name__ == '__main__':
    main()
