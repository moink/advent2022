import copy
import math

import advent_tools


def main():
    # advent_tools.TESTING = True
    data = advent_tools.read_all_integers()
    # data = advent_tools.read_whole_input()
    # data = advent_tools.read_input_lines()
    # data = advent_tools.read_input_no_strip()
    # data = advent_tools.read_dict_from_input_file(sep=' => ', key='left')
    # data = advent_tools.read_dict_of_list_from_file(sep=' => ', key='left')
    # data = advent_tools.read_one_int_per_line()
    # data = advent_tools.PlottingGrid.from_file({'.' : 0, '#' : 1})
    # data = advent_tools.read_input_line_groups()
    # data = advent_tools.read_nparray_from_digits()
    data = process_input(data)
    # print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    result = {}
    for (blueprint_num, ore_ore_cost, clay_ore_cost, obsidian_ore_cost,
         obsidian_clay_cost, geode_ore_cost, geode_obsidian_cost) in data:
        result[blueprint_num] = {
            "ore": {"ore": ore_ore_cost},
            "clay": {"ore": clay_ore_cost},
            "obsidian": {"ore": obsidian_ore_cost, "clay": obsidian_clay_cost},
            "geode": {"ore": geode_ore_cost, "obsidian": geode_obsidian_cost},
        }
    return result


def run_part_1(data):
    return sum(blueprint_num * get_max_geodes(blueprint, 24)
               for blueprint_num, blueprint in data.items())

def run_part_2(data):
    return math.prod(get_max_geodes(data[i], 32) for i in range(1, 4))


def get_max_geodes(blueprint, max_steps):
    start_robots = {
        "ore": 1,
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
    }
    start_materials = {
        "ore": 0,
        "clay": 0,
        "obsidian": 0,
        "geode": 0,
    }
    start_state = RobotState(blueprint, start_robots, start_materials)
    end_points = advent_tools.get_all_states_in_steps(start_state, max_steps)
    max_geodes = max(state.materials["geode"] for state in end_points)
    return max_geodes


def sum_dicts(materials, collected):
    return {key: materials.get(key, 0) + collected.get(key, 0)
              for key in list(materials.keys()) + list(collected.keys())}


class RobotState(advent_tools.StateForGraphs):

    def __init__(self, blueprint, robots, materials):
        self.blueprint = blueprint
        self.robots = copy.deepcopy(robots)
        self.materials = copy.deepcopy(materials)

    def __str__(self):
        return f"Robots: {self.robots} Materials: {self.materials}\n"

    def is_final(self):
        return False

    def possible_next_states(self):
        collected = {
            robot_type: robot_count for robot_type, robot_count in self.robots.items()
        }
        geode_robot = self.build_one_robot(collected, "geode")
        if geode_robot:
            return {geode_robot}
        obsidian_robot = self.build_one_robot(collected, "obsidian")
        if obsidian_robot:
            return {obsidian_robot}
        next_states = {RobotState(self.blueprint, self.robots,
                           sum_dicts(self.materials, collected))}
        for robot_type in ["ore", "clay"]:
            robot = self.build_one_robot(collected, robot_type)
            if robot:
                next_states.add(robot)
        return next_states

    def build_one_robot(self, collected, robot_type):
        costs = self.blueprint[robot_type]
        if all(self.materials[material] >= cost for material, cost in costs.items()):
            new_materials = copy.deepcopy(self.materials)
            new_robots = copy.deepcopy(self.robots)
            for material, cost in costs.items():
                new_materials[material] -= cost
            new_robots[robot_type] += 1
            return RobotState(
                self.blueprint, new_robots, sum_dicts(new_materials, collected)
            )
        return None


if __name__ == '__main__':
    main()
