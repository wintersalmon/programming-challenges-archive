from sys import stdin


def solution(step):
    row = 1
    while True:
        if (row - 1) * (row - 1) < step <= row * row:
            break
        row += 1

    row_center_step = row * row - row + 1
    step_offset_from_row_center = step - row_center_step

    # print(idx, row_center_step, step_offset_from_row_center)

    x, y = row, row
    if step_offset_from_row_center == 0:
        x, y = row, row
    elif row % 2:  # odd dim, right bottom - > top left
        if step_offset_from_row_center > 0:
            x -= step_offset_from_row_center
        else:
            y += step_offset_from_row_center
    else:  # even dim, top left -> right bottom
        if step_offset_from_row_center > 0:
            y -= step_offset_from_row_center
        else:
            x += step_offset_from_row_center

    return x, y


def read_input():
    while True:
        line = next(stdin)
        idx = int(line)
        if idx == 0:
            raise StopIteration
        else:
            yield idx


def main():
    for idx in read_input():
        row, col = solution(idx)
        print('{} {}'.format(row, col))


if __name__ == '__main__':
    main()
    # print(solution(1), (1, 1))
    # print(solution(2), (1, 2))
    # print(solution(3), (2, 2))
    # print(solution(4), (2, 1))
    # print(solution(5), (3, 1))
    # print(solution(6), (3, 2))
    # print(solution(7), (3, 3))
    # print(solution(8), (2, 3))
    # print(solution(9), (1, 3))
    # print(solution(10), (1, 4))
    # print(solution(20), (5, 4))
    # print(solution(25), (1, 5))
