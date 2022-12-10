import math

import advent_tools


def main():
    data = advent_tools.read_input_lines()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    result = []
    for line in data:
        letter, number = line.split()
        result.append((letter, int(number)))
    return result


def run_part_1(data):
    return run_rope_simulation(data, 2)


def run_part_2(data):
    return run_rope_simulation(data, 10)


def run_rope_simulation(instructions, num_knots):
    x = [0] * num_knots
    y = [0] * num_knots
    tail_positions = set()
    for direction, dist in instructions:
        for _ in range(dist):
            x[0], y[0] = take_one_step(direction, x[0], y[0])
            for k in range(1, num_knots):
                x[k], y[k] = follow_knot(x[k - 1], y[k - 1], x[k], y[k])
            tail_positions.add((x[-1], y[-1]))
    return len(tail_positions)


def take_one_step(direction, head_x, head_y):
    match direction:
        case 'R':
            head_x += 1
        case 'L':
            head_x -= 1
        case 'U':
            head_y -= 1
        case 'D':
            head_y += 1
    return head_x, head_y


def follow_knot(head_x, head_y, tail_x, tail_y):
    if head_y == tail_y:
        if abs(head_x - tail_x) > 1:
            tail_x += math.copysign(1, head_x - tail_x)
    elif head_x == tail_x:
        if abs(head_y - tail_y) > 1:
            tail_y += math.copysign(1, head_y - tail_y)
    if abs(head_x - tail_x) > 1 or abs(head_y - tail_y) > 1:
        tail_x += math.copysign(1, head_x - tail_x)
        tail_y += math.copysign(1, head_y - tail_y)
    return tail_x, tail_y


if __name__ == '__main__':
    main()
