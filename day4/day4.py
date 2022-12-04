import advent_tools


def main():
    data = advent_tools.read_all_integers()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    return [[abs(val) for val in line] for line in data]


def run_part_1(data):
    return sum((start1 <= start2 and end1 >= end2)
               or (start2 <= start1 and end2 >= end1)
               for start1, end1, start2, end2 in data)


def run_part_2(data):
    return sum((start1 <= end2 and end1 >= start2)
               or (start2 <= end1 and end2 >= start1)
               for start1, end1, start2, end2 in data)


if __name__ == '__main__':
    main()
