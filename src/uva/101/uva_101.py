from sys import stdin


def read_input():
    number_of_blocks = int(next(stdin))
    instructions = list()

    while True:
        instruction = next(stdin).rstrip('\r\n')
        if instruction == 'quit':
            break
        else:
            instructions.append(instruction)

    return number_of_blocks, instructions


def main():
    number_of_blocks, instructions = read_input()

    blocks = solution(number_of_blocks, instructions)

    blocks = [[str(i) for i in items] for items in blocks]
    for i, b in enumerate(blocks):
        if b:
            fmt_line = '{}: {}'.format(i, ' '.join(b))
        else:
            fmt_line = '{}:'.format(i)
        print(fmt_line)


QUIT = 'quit'
MOVE = 'move'
PILE = 'pile'
ONTO = 'onto'
OVER = 'over'


def solution(number_of_blocks, instructions):
    block_position = {i: i for i in range(number_of_blocks)}
    block_status = [[i] for i in range(number_of_blocks)]

    for instruction in instructions:
        ins = instruction.split()
        first_command, second_command = ins[0], ins[2]
        src_block, dst_block = int(ins[1]), int(ins[3])
        src_pos, dst_pos = block_position[src_block], block_position[dst_block]

        if src_pos == dst_pos:
            continue

        if first_command == MOVE:  # return all src tops
            while block_status[src_pos][-1] != src_block:
                top = block_status[src_pos].pop()
                block_status[top].append(top)
                block_position[top] = top

        if second_command == ONTO:  # return all dst tops
            while block_status[dst_pos][-1] != dst_block:
                top = block_status[dst_pos].pop()
                block_status[top].append(top)
                block_position[top] = top

        if first_command == MOVE:  # move src to dst
            block_status[src_pos].pop()
            block_status[dst_pos].append(src_block)
            block_position[src_block] = dst_pos

        elif first_command == PILE:  # move src stack to dst
            temp_block = list()
            while block_status[src_pos][-1] != src_block:
                temp_block.append(block_status[src_pos].pop())
            temp_block.append(block_status[src_pos].pop())
            while temp_block:
                item = temp_block.pop()
                block_status[dst_pos].append(item)
                block_position[item] = dst_pos

    return block_status


if __name__ == '__main__':
    main()
