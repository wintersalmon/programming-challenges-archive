from sys import stdin

"""
Ant on a Chessboard
UVa: 10161
programming-challenges PR_089

make new coord method
first row is (1,1)
the surrounding blocks of current row becomes next row
here are some rules about row

# number of steps in row: row * 2 - 1
# row center step value: row * row - row + 1
# row max step value: row * row

# how to solve
1. use step to figure out current row
2. set x, y = row, row
3. figure out offset of (current_step, current_row_center_step)
4. handle (x, y) changes according to row(even,odd), offset(zero,plus,minus) : 5 cases
    1. offset(zero)
    2. row(odd),offset(plus)
    3. row(odd),offset(minus)
    4. row(even),offset(plus)
    5. row(even),offset(minus)
"""


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
