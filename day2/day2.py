import advent_tools
import unittest


def main():
    data = advent_tools.read_input_lines()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


scores = {
    "A": 1,
    "B": 2,
    "C": 3,
    "X": 1,
    "Y": 2,
    "Z": 3,
}


def process_input(data):
    result = [line.split() for line in data]
    return result


def run_part_1(data):
    total = 0
    for theirs, mine in data:
        their_score = scores[theirs]
        my_score = scores[mine]
        total += my_score
        total += get_win_points(their_score, my_score)
    return total


def run_part_2(data):
    total = 0
    for theirs, win_condition in data:
        their_score = scores[theirs]
        my_score = get_my_play(their_score, win_condition)
        total += my_score
        total += get_win_points(their_score, my_score)
    return total


def get_win_points(their_score, my_score):
    delta = (my_score - their_score) % 3
    if delta == 0:
        return 3
    elif delta ==1:
        return 6
    elif delta == 2:
        return 0


def get_my_play(their_score, win_condition):
    if win_condition == "X":
        my_score = (their_score + 1) % 3 + 1
    elif win_condition == "Y":
        my_score = their_score
    else:
        my_score = their_score % 3 + 1
    return my_score

class AdventTests(unittest.TestCase):

    def test_get_win_points(self):
        test_cases = [
            ("A", "X", 3),  # rock, rock, draw
            ("A", "Y", 6),  # rock, paper, win
            ("A", "Z", 0),  # rock, scissors, lose
            ("B", "X", 0),  # paper, rock, lose
            ("B", "Y", 3),  # paper, paper, draw
            ("B", "Z", 6),  # paper, scissors, win
            ("C", "X", 6),  # scissors, rock, win
            ("C", "Y", 0),  # scissors, paper, lose
            ("C", "Z", 3),  # scissors, scissors, draw
        ]
        for theirs, mine, expected_result in test_cases:
            their_score = scores[theirs]
            my_score = scores[mine]
            result = get_win_points(their_score, my_score)
            self.assertEqual(expected_result, result, msg=f"{theirs}, {mine}")

    def test_winning_conditions(self):
        test_cases = [
            ("A", "X", 3),  # rock, lose, scissors
            ("A", "Y", 1),  # rock, draw, rock
            ("A", "Z", 2),  # rock, win, paper
            ("B", "X", 1),  # paper, lose, rock
            ("B", "Y", 2),  # paper, draw, paper
            ("B", "Z", 3),  # paper, win, scissors
            ("C", "X", 2),  # scissors, lose, paper
            ("C", "Y", 3),  # scissors, draw, scissors
            ("C", "Z", 1),  # scissors, win, rock
        ]
        for theirs, win_condition, expected_result in test_cases:
            their_score = scores[theirs]
            result = get_my_play(their_score, win_condition)
            self.assertEqual(expected_result, result, msg=f"{theirs}, {win_condition}")


if __name__ == '__main__':
    main()
    unittest.main()
