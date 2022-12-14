import itertools
import json

import advent_tools


def main():
    data = advent_tools.read_input_line_groups()
    data = process_input(data)
    print('Part 1:', run_part_1(data))
    print('Part 2:', run_part_2(data))


def process_input(data):
    result = [(MessagePacket(line1), MessagePacket(line2)) for line1, line2 in data]
    return result


def run_part_1(data):
    return sum(i if left < right else 0 for i, (left, right) in enumerate(data, 1))


def run_part_2(data):
    packets = [packet for group in data for packet in group]
    divider1 = MessagePacket([[2]])
    divider2 = MessagePacket([[6]])
    packets.extend([divider1, divider2])
    packets.sort()
    return (packets.index(divider1) + 1) * (packets.index(divider2) + 1)


class MessagePacket:

    def __init__(self, signal):
        if isinstance(signal, str):
            self.packet = json.loads(signal)
        else:
            self.packet = signal

    def __str__(self):
        return str(self.packet)

    def __repr__(self):
        return str(self.packet)

    def __eq__(self, other):
        return str(self) == str(other)

    def __lt__(self, other):
        if self.packet is None:
            return True
        if other.packet is None:
            return False
        if isinstance(self.packet, int) and isinstance(other.packet, int):
            return self.packet < other.packet
        if isinstance(self.packet, list) and isinstance(other.packet, int):
            return self < MessagePacket([other.packet])
        if isinstance(self.packet, int) and isinstance(other.packet, list):
            return MessagePacket([self.packet]) < other
        for left, right in itertools.zip_longest(self.packet, other.packet):
            if MessagePacket(left) < MessagePacket(right):
                return True
            if MessagePacket(right) < MessagePacket(left):
                return False
        return False


if __name__ == '__main__':
    main()
