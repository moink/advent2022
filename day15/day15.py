import collections

import advent_tools


def main():
    data = advent_tools.read_all_integers()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    return {(x_s, y_s): (x_b, y_b) for x_s, y_s, x_b, y_b in data}


def run_part_1(data):
    covered = set()
    if advent_tools.TESTING:
        y = 10
    else:
        y = 2000000
    for sensor, beacon in data.items():
        dist = manhattan_distance(sensor, beacon)
        (x_s, y_s) = sensor
        if y_s - dist <= y <= y_s + dist:
            for x in range(x_s - dist - 1, x_s + dist + 1):
                if manhattan_distance(sensor, (x, y)) <= dist:
                    covered.add((x, y))
    covered.difference_update(data.keys())
    covered.difference_update(data.values())
    return len(covered)


def manhattan_distance(pt1, pt2):
    (x_s, y_s) = pt1
    (x_b, y_b) = pt2
    dist = abs(x_b - x_s) + abs(y_b - y_s)
    return dist


def zone_size(zone):
    min_x, max_x, min_y, max_y = zone
    return (max_y - min_y + 1) * (max_x - min_x + 1)


def run_part_2(data):
    if advent_tools.TESTING:
        size = 20
    else:
        size = 4000000
    x, _, y, _ = find_uncovered(data, size)
    return 4000000 * x + y



def find_uncovered(data, size):
    min_x = min_y = 0
    max_x = max_y = size
    to_evaluate = collections.deque([(min_x, max_x, min_y, max_y)])
    while to_evaluate:
        zone = to_evaluate.popleft()
        size = zone_size(zone)
        if size == 1:
            return zone
        if size > 1:
            for sub_zone in split_zone(zone):
                if any_part_of_zone_unseen_by_all_beacons(sub_zone, data):
                    to_evaluate.append(sub_zone)
    raise RuntimeError("got to end")

def split_zone(zone):
    min_x, max_x, min_y, max_y = zone
    mid_x = (max_x + min_x) // 2
    mid_y = (max_y + min_y) // 2
    if mid_x >= min_x:
        if mid_y >= min_y:
            yield min_x, mid_x, min_y, mid_y
        if max_y >= mid_y + 1:
            yield min_x, mid_x, mid_y + 1, max_y
    if max_x >= mid_x + 1:
        if mid_y >= min_y:
            yield mid_x + 1, max_x, min_y, mid_y
        if max_y >= mid_y + 1:
            yield mid_x + 1, max_x, mid_y + 1, max_y

def any_part_of_zone_unseen_by_all_beacons(zone, data):
    return all(any_part_of_zone_unseen_by_beacon(zone, sensor, beacon)
               for sensor, beacon in data.items())

def any_part_of_zone_unseen_by_beacon(zone, sensor, beacon):
    dist = manhattan_distance(sensor, beacon)
    min_x, max_x, min_y, max_y = zone
    corners = [(min_x, min_y), (min_x, max_y), (max_x, min_y), (max_x, max_y)]
    max_dist = max(
        manhattan_distance(corner, sensor) for corner in corners
    )
    return max_dist > dist


if __name__ == '__main__':
    main()
