import collections
import re


def main():
    stack_part, instruction_part = read_input_file()
    stack = parse_stack(stack_part)
    instructions = parse_instructions(instruction_part)
    print('Part 1:', run_part_1(stack, instructions))
    stack = parse_stack(stack_part)
    print('Part 2:', run_part_2(stack, instructions))


def read_input_file():
    with open("input.txt") as in_file:
        contents = in_file.read()
    return [group.splitlines() for group in contents.split("\n\n")]


def parse_stack(lines):
    stack = collections.defaultdict(collections.deque)
    stack_names = [int(char) for char in lines[-1][1::4]]
    for line in lines[-2::-1]:
        for name, char in zip(stack_names, line[1::4]):
            if char != " ":
                stack[name].append(char)
    return dict(stack)


def parse_instructions(lines):
    return [tuple(int(char) for char in re.findall(r'[0-9]+', line)) for line in lines]


def run_part_1(stack, instructions):
    for num_to_move, from_stack, to_stack in instructions:
        for i in range(num_to_move):
            stack[to_stack].append(stack[from_stack].pop())
    return get_top_of_stack(stack)


def get_top_of_stack(stack):
    return "".join(col.pop() for col in stack.values())


def run_part_2(stack, instructions):
    for num_to_move, from_stack, to_stack in instructions:
        crane = reversed([stack[from_stack].pop() for _ in range(num_to_move)])
        stack[to_stack].extend(crane)
    return get_top_of_stack(stack)


if __name__ == '__main__':
    main()
