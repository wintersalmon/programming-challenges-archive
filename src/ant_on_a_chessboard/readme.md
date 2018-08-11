# Ant on a Chessboard
- UVa: 10161
- Programming Challenges Problem 89

## Solution

- make new coord method
- first row is (1,1)
- the surrounding blocks of current row becomes next row
- here are some rules about row

-

- number of steps in row: row * 2 - 1
- row center step value: row * row - row + 1
- row max step value: row * row

-

### how to solve
1. use step to figure out current row
2. set x, y = row, row
3. figure out offset of (current_step, current_row_center_step)
4. handle (x, y) changes according to row(even,odd), offset(zero,plus,minus) : 5 cases
    1. offset(zero)
    2. row(odd),offset(plus)
    3. row(odd),offset(minus)
    4. row(even),offset(plus)
    5. row(even),offset(minus)
