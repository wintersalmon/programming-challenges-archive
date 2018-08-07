from collections import namedtuple
from sys import stdin

QUIT = 'quit'
MOVE = 'move'
PILE = 'pile'
ONTO = 'onto'
OVER = 'over'

Event = namedtuple('Event', ['command', 'src', 'option', 'dst'])


def return_all_blocks_above_src(positions, blocks, src):
    src_pos = positions[src]
    src_block = blocks[src_pos]
    while src_block[-1] != src:
        top = src_block.pop()
        blocks[top].append(top)
        positions[top] = top


def move_all_blocks_consisting_src_to_dst(positions, blocks, src, dst):
    src_pos = positions[src]
    src_block = blocks[src_pos]
    dst_pos = positions[dst]
    dst_block = blocks[dst_pos]

    temp_block = list()
    while src_block[-1] != src:
        temp_block.append(src_block.pop())

    temp_block.append(src_block.pop())

    while temp_block:
        item = temp_block.pop()
        dst_block.append(item)
        positions[item] = dst_pos


def solution(number_of_blocks, events):
    blocks = [[i] for i in range(number_of_blocks)]
    positions = {i: i for i in range(number_of_blocks)}

    for event in events:
        command = event.command
        option = event.option
        src = event.src
        dst = event.dst

        if positions[src] == positions[dst]:  # SKIP current instruction
            continue

        if command == MOVE:  # RETURN all values above src to their INITIAL stack
            return_all_blocks_above_src(positions, blocks, src)

        if option == ONTO:  # RETURN all values above dst to their INITIAL stack
            return_all_blocks_above_src(positions, blocks, dst)

        move_all_blocks_consisting_src_to_dst(positions, blocks, src, dst)

    return blocks


def read_input():
    number_of_blocks = int(next(stdin))
    events = list()

    while True:
        raw_event = next(stdin).rstrip('\r\n')
        if raw_event == QUIT:
            break
        else:
            command, raw_src, option, raw_dst = raw_event.split()
            decoded_event = Event(command=command, src=int(raw_src), option=option, dst=int(raw_dst))
            events.append(decoded_event)

    return number_of_blocks, events


def print_result(blocks):
    for i, block in enumerate(blocks):
        if block:
            fmt_line = '{}: {}'.format(i, ' '.join(str(i) for i in block))
        else:
            fmt_line = '{}:'.format(i)
        print(fmt_line)


def main():
    number_of_blocks, events = read_input()

    blocks = solution(number_of_blocks, events)

    print_result(blocks)


if __name__ == '__main__':
    main()
