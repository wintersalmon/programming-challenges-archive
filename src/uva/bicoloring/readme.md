# Bicoloring

- Uva: 10004
- Programming Challenges Problem 65 (Chapter 09)

## Solution

1. start from any node[0] and paint with color_1

2. if node is not painted yet

    1. paint current node
    2. paint all child with different color
    3. return True if all child paint was success

3. if node is already painted with same color return True

4. if node is already painted with different color return False
