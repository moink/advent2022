import advent_tools


def main():
    data = advent_tools.read_input_lines()
    record = run_program(data)
    print('Part 1:', run_part_1(record))
    run_part_2(record)


def run_part_1(record):
    return sum(
        cycle_num * extract_record_on_cycle(record, cycle_num)
        for cycle_num in range(20, 221, 40)
    )


def run_part_2(record):
    grid = advent_tools.PlottingGrid((6, 40))
    for cycle_num in range(241):
        register = extract_record_on_cycle(record, cycle_num + 1)
        crt_pos = cycle_num % 40
        if abs(register - crt_pos) < 2:
            grid[cycle_num // 40, crt_pos] = 1
    grid.show()


def run_program(data):
    register = 1
    cycle = 1
    record = {0: register}
    for line in data:
        if line.startswith("noop"):
            cycle += 1
        else:
            _, num = line.split()
            cycle += 2
            register += int(num)
            record[cycle] = register
    return record


def extract_record_on_cycle(record, cycle_num):
    return record[max(filter(lambda x: x <= cycle_num, record.keys()))]


if __name__ == '__main__':
    main()
