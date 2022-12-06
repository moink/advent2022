import collections
import unittest

import advent_tools


def main():
    data = advent_tools.read_whole_input()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    return find_marker(data, 4)


def run_part_2(data):
    return find_marker(data, 14)


def find_marker(data_stream, marker_len=4):
    most_recent_n = collections.deque(maxlen=marker_len)
    for count, char in enumerate(data_stream):
        most_recent_n.append(char)
        if len(set(most_recent_n)) == marker_len:
            return count + 1


class TestDaySix(unittest.TestCase):

    def test_find_marker(self):
        test_cases = [
            ("bvwbjplbgvbhsrlpgdmjqwftvncz", 5),
            ("nppdvjthqldpwncqszvftbrmjlhg", 6),
            ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 10),
            ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 11),
            ]
        for data_stream, expected_result in test_cases:
            result = find_marker(data_stream, 4)
            self.assertEqual(expected_result, result)
        test_cases = [
            ("mjqjpqmgbljsphdztnvjfqwrcgsmlb", 19),
            ("bvwbjplbgvbhsrlpgdmjqwftvncz", 23),
            ("nppdvjthqldpwncqszvftbrmjlhg", 23),
            ("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 29),
            ("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 26),
        ]
        for data_stream, expected_result in test_cases:
            result = find_marker(data_stream, 14)
            self.assertEqual(expected_result, result)


if __name__ == '__main__':
    main()
    unittest.main()
