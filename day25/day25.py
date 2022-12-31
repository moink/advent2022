import advent_tools

BASE = 5
DIGIT_VALUES = {
    "=": -2,
    "-": -1,
    "0": 0,
    "1": 1,
    "2": 2
}

VALUE_DIGITS = {val % BASE: key for key, val in DIGIT_VALUES.items()}


def main():
    data = advent_tools.read_input_lines()
    print('Part 1:', run_part_1(data))


def run_part_1(data):
    return convert_dec_to_snafu(sum(convert_snafu_to_dec(line) for line in data))


def convert_snafu_to_dec(snafu_str):
    return sum(
        DIGIT_VALUES[digit] * BASE ** power
        for power, digit in enumerate(reversed(snafu_str))
    )


def convert_dec_to_snafu(num):
    lowest_digit = VALUE_DIGITS[(num % BASE)]
    rest_of_number = num - DIGIT_VALUES[lowest_digit]
    if rest_of_number == 0:
        return lowest_digit
    else:
        return "".join((convert_dec_to_snafu(rest_of_number // BASE), lowest_digit))


if __name__ == '__main__':
    main()
