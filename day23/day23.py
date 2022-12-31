import advent_tools


def main():
    data = advent_tools.read_input_lines()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    elves = set()
    for y_pos, line in enumerate(data):
        for x_pos, char in enumerate(line):
            if char == "#":
                elves.add((x_pos, y_pos))
    return elves


class North:

    @staticmethod
    def places_to_check(x, y):
        return {(x, y - 1), (x - 1, y - 1), (x + 1, y - 1)}

    @staticmethod
    def place_to_move(x, y):
        return x, y - 1


class South:

    @staticmethod
    def places_to_check(x, y):
        return {(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)}

    @staticmethod
    def place_to_move(x, y):
        return x, y + 1


class East:

    @staticmethod
    def places_to_check(x, y):
        return {(x + 1, y), (x + 1, y - 1), (x + 1, y + 1)}

    @staticmethod
    def place_to_move(x, y):
        return x + 1, y


class West:

    @staticmethod
    def places_to_check(x, y):
        return {(x - 1, y), (x - 1, y - 1), (x - 1, y + 1)}

    @staticmethod
    def place_to_move(x, y):
        return x - 1, y


def adjacent_places(x, y):
    cycle = [North(), South(), West(), East()]
    return set.union(*(direction.places_to_check(x, y) for direction in cycle))


def run_part_1(elves):
    return run_simulation(elves, 10)


def run_part_2(elves):
    return run_simulation(elves, 2000)


def run_simulation(elves, num_steps):
    cycle = [North(), South(), West(), East()]
    for step in range(num_steps):
        any_elf_moves = False
        proposal = {}
        for x, y in elves:
            if elves.intersection(adjacent_places(x, y)):
                for direction in cycle:
                    if not elves.intersection(direction.places_to_check(x, y)):
                        proposal[(x, y)] = direction.place_to_move(x, y)
                        break
                    else:
                        proposal[(x, y)] = x, y
            else:
                proposal[(x, y)] = x, y
        elves = set()
        for cur_pos, pro_pos in proposal.items():
            other_prop = {val for key, val in proposal.items() if key != cur_pos}
            if pro_pos in other_prop:
                elves.add(cur_pos)
            else:
                elves.add(pro_pos)
                if cur_pos != pro_pos:
                    any_elf_moves = True
        cycle = [*cycle[1:], cycle[0]]
        print(step, "...")
        if not any_elf_moves:
            return step + 1  # Part 2
    max_x, max_y, min_x, min_y = get_rectangle(elves)
    return (max_y - min_y) * (max_x - min_x) - len(elves)  # Part 1


def visualize_rectangle(elves):
    max_x, max_y, min_x, min_y = get_rectangle(elves)
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            if (x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print("\n", end="")
    print("")


def get_rectangle(elves):
    all_x = {elf[0] for elf in elves}
    all_y = {elf[1] for elf in elves}
    min_x = min(all_x)
    max_x = max(all_x)
    min_y = min(all_y)
    max_y = max(all_y)
    return max_x + 1, max_y + 1, min_x, min_y


if __name__ == '__main__':
    main()
