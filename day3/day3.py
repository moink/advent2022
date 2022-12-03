import unittest

import advent_tools


def main():
    data = advent_tools.read_input_lines()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    result = 0
    for line in data:
        split_place = len(line) // 2
        first_half, second_half = set(line[:split_place]), set(line[split_place:])
        in_both = first_half.intersection(second_half)
        letter = get_one_item(in_both)
        result += get_priority(letter)
    return result


def get_one_item(intersection):
    if len(intersection) != 1:
        raise RuntimeError(
            f"Intersection '{intersection}' does not contain exactly one item"
        )
    letter = intersection.pop()
    return letter


def run_part_2(data):
    result = 0
    for group in (data[pos:pos + 3] for pos in range(0, len(data), 3)):
        overlap = set.intersection(*(set(line) for line in group))
        letter = get_one_item(overlap)
        result += get_priority(letter)
    return result


def get_priority(letter):
    if letter.islower():
        return ord(letter) - 96
    return ord(letter) - 38


class TestDayThree(unittest.TestCase):

    def test_get_priority(self):
        test_cases = [
            ("p", 16),
            ("L", 38),
            ("P", 42),
            ("v", 22),
            ("t", 20),
            ("s", 19),
        ]
        for letter, expected_result in test_cases:
            result = get_priority(letter)
            msg = f"Wrong answer for '{letter}', difference is {expected_result - result}"
            self.assertEqual(expected_result, result, msg=msg)


if __name__ == '__main__':
    main()
    unittest.main()
