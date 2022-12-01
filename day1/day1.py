import advent_tools


def main():
    data = advent_tools.read_input_line_groups()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    result = []
    for group in data:
        result.append([int(cals) for cals in group])
    return result


def run_part_1(data):
    elves = [sum(group) for group in data]
    return(max(elves))


def run_part_2(data):
    elves = [sum(group) for group in data]
    return sum(sorted(elves)[-3:])


if __name__ == '__main__':
    main()
