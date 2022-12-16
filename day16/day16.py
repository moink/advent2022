import collections
import itertools

import advent_tools


def main():
    print('Part 1:', run_part_1())
    print('Part 2:', run_part_2())


def process_input(data):
    result = {}
    for line in data:
        line = line.replace("valve ", "valves")
        left, right = line.split("valves")
        destinations = [dest.strip() for dest in right.split(",")]
        _, room, _, _, rest = left.split(" ", maxsplit=4)
        rate = rest.split("=")[1].split(";")[0]
        result[room] = (int(rate), destinations)
    return result


def run_part_1():
    scores = get_best_scores(30)
    return max(scores.values())


def run_part_2():
    scores = get_best_scores(26)
    return max(
        my_score + elephant_score
        for (my_valves, my_score), (elephant_steps, elephant_score)
        in itertools.combinations(scores.items(), 2)
        if not my_valves.intersection(elephant_steps)
    )


def get_best_scores(max_steps):
    discovered = explore_map(max_steps)
    max_scores = collections.defaultdict(set)
    for state, scores in discovered.items():
        max_score = max(score for _, score in scores)
        if max_score > 0:
            max_scores[frozenset(state.opened_valves)].add(max_score)
    return {open_valves: max(scores) for open_valves, scores in max_scores.items()}


def explore_map(max_steps):
    initial_state = ValveState("AA", set())
    queue = collections.deque()
    discovered = collections.defaultdict(ParetoSet)
    discovered[initial_state].add((0, 0))
    queue.append((initial_state, 0, 0))
    while queue:
        state, num_steps, score = queue.popleft()
        new_states = state.possible_next_states()
        for new_state, delta_flow in new_states:
            delta_score = (max_steps - num_steps - 1) * delta_flow
            if num_steps < max_steps:
                if discovered[new_state].add((num_steps + 1, score + delta_score)):
                    queue.append((new_state, num_steps + 1, score + delta_score))
    return discovered


class ParetoSet(set):

    def add(self, element):
        add_it = True
        steps, score = element
        for other_steps, other_score in self:
            if other_steps <= steps and other_score >= score:
                add_it = False
        if add_it:
            super().add(element)
        return add_it


class ValveState(advent_tools.StateForGraphs):
    maze = process_input(advent_tools.read_input_lines())

    def __init__(self, pos, opened_valves):
        self.pos = pos
        self.opened_valves = opened_valves

    def __str__(self):
        return "_".join([self.pos, "-".join(sorted(self.opened_valves))])

    def is_final(self):
        return False

    def possible_next_states(self):
        result = {
            (ValveState(new_pos, self.opened_valves), 0)
            for new_pos in self.maze[self.pos][1]
            if new_pos not in {v for v, _ in self.opened_valves}
        }
        delta_flow = self.maze[self.pos][0]
        if self.pos not in self.opened_valves and delta_flow > 0:
            result.add((
                ValveState(self.pos, self.opened_valves.union({self.pos})), delta_flow
            ))
        return result


if __name__ == '__main__':
    main()
