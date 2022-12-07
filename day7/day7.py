from dataclasses import dataclass, field

import advent_tools


@dataclass
class Directory:
    name: str
    subdirectories: dict[str, 'Directory'] = field(default_factory=dict)
    files: dict[str, int] = field(default_factory=dict)
    parent: 'Directory' = None


def main():
    data = advent_tools.read_input_lines()
    tree = process_input(data)
    all_sizes = get_all_dir_sizes(tree)
    print('Part 1:', run_part_1(all_sizes))
    print('Part 2:', run_part_2(all_sizes))


def process_input(data):
    tree = Directory("/")
    cur_node = tree
    for line in data[2:]:
        if line.startswith("$ ls"):
            continue
        if line.startswith("$ cd .."):
            cur_node = cur_node.parent
        elif line.startswith("$ cd"):
            _, _, dir_name = line.split()
            cur_node = cur_node.subdirectories[dir_name]
        elif line.startswith("dir"):
            _, dir_name = line.split()
            cur_node.subdirectories[dir_name] = Directory(dir_name, parent=cur_node)
        else:
            size, filename = line.split()
            cur_node.files[filename] = int(size)
    return tree


def get_total_size(directory: Directory, all_sizes):
    total_size = (
        sum(directory.files.values())
        + sum(get_total_size(subdir, all_sizes)
              for subdir in directory.subdirectories.values()))
    all_sizes.append(total_size)
    return total_size


def get_all_dir_sizes(tree):
    all_sizes = []
    get_total_size(tree, all_sizes)
    return all_sizes


def run_part_1(all_sizes):
    return sum(filter(lambda x: x <= 100000, all_sizes))


def run_part_2(all_sizes):
    available = 70000000
    need_free = 30000000
    total_used = max(all_sizes)
    need_to_free = total_used - available + need_free
    return min(filter(lambda x: x > need_to_free, all_sizes))


if __name__ == '__main__':
    main()
