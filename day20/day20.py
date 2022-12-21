import advent_tools


def main():
    data = advent_tools.read_one_int_per_line()
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def run_part_1(data):
    nodes, zero_node = process_input(data, 1)
    mix_nodes(nodes)
    return get_coordinate(zero_node)


def run_part_2(data):
    nodes, zero_node = process_input(data, 811589153)
    for _ in range(10):
        mix_nodes(nodes)
    return get_coordinate(zero_node)


def process_input(data, multiplier):
    nodes = []
    zero_node = None
    for num in data:
        node = advent_tools.LinkedListNode(num * multiplier)
        nodes.append(node)
        if num == 0:
            zero_node = node
    num_nodes = len(nodes)
    for i in range(num_nodes - 1):
        nodes[i].next = nodes[i + 1]
    for i in range(1, num_nodes):
        nodes[i].previous = nodes[i - 1]
    nodes[num_nodes - 1].next = nodes[0]
    nodes[0].previous = nodes[num_nodes - 1]
    return nodes, zero_node


def mix_nodes(nodes):
    for node in nodes:
        steps = abs(node.data) % (len(nodes) - 1)
        if node.data > 0:
            for _ in range(steps):
                reorder_nodes(node.previous, node.next, node, node.next.next)
        else:
            for _ in range(steps):
                reorder_nodes(node.previous.previous, node, node.previous, node.next)


def reorder_nodes(first, second, third, fourth):
    re_attach_nodes(first, second)
    re_attach_nodes(second, third)
    re_attach_nodes(third, fourth)


def re_attach_nodes(left, right):
    left.next = right
    right.previous = left


def get_coordinate(zero_node):
    return sum(get_nth_node(zero_node, 1000 * n) for n in range(1, 4))


def get_nth_node(start_node, num_steps):
    cur_node = start_node
    for _ in range(num_steps):
        cur_node = cur_node.next
    return cur_node.data


if __name__ == '__main__':
    main()
