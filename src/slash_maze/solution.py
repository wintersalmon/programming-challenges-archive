"""
Slash Maze
Uva: 705
programming-challenges Chapter09 PR_068


1. 입력된 미로를 적절한 자료구조로 표현한다

- `Maze`는 3가지의 좌표 시스템으로 표현된다
    1) tile 좌표계: 입력된 값의 좌표
    2) node_hor 좌표계: `tile`의 좌우에 위치한 노드를 표현하기 위한 좌표계
    3) node_ver 좌표계: `tile`의 상하에 위치한 노드를 표현하기 위한 좌표계

- `tile`값에 따라서 주변에 있는 노드를 적절하게 연결해준다
    1) tile == '/'
        - up + left
        - down + right
    2) tile == '\'
        - up + right
        - down + left

2. 미로의 각 노드를 DFS 탐색하며 CYCLE 의 유무를 확인한다
    - 각 노드는 정확히 한개의 그룹에 포함되어 있기 때문에 한번 확인한 노드는 다시 확인하지 않는다
    - 방문한 결과 노드의 개수가(중복되지 않은) 4개 이상이고 (최소 사이클의 크기), 인접 노드가 정확히 2개씩 있다면 CYCLE 이다


## Maze Examples

### input

3 3
///
\//
\\\


### sizes

|          | max_row | max_col |
|----------|---------|---------|
| tile     | n       | m       |
| node_ver | n       | m - 1   |
| node_hor | n - 1   | m       |

|          | max_row | max_col |
|----------|---------|---------|
| tile     | 3       | 3       |
| node_ver | 3       | 2       |
| node_hor | 2       | 3       |


### coordinate
- (n, m): tile
- [n, m]: node_hor
- <n, m>: node_ver


(0 0)   [0 0]   (0 1)   [0 1]   (0 2)

<0 0>           <0 1>           <0 2>

(1 0)   [1 0]   (1 1)   [1 1]   (1 2)

<1 0>           <1 1>           <1 2>

(2 0)   [2 0]   (2 1)   [2 1]   (2 2)


### convert tile coordinate to adjacent node coordinate

- tile          n, m
- node_up       n - 1, m
-node_right     n, m
- node_down     n, m
- node_left     n, m - 1


            <n-1, m>

[n, m-1]    (n, m)      [n, m]

            <n, m>
"""
from sys import stdin


class Node(object):
    def __init__(self, number):
        self.number = number
        self.adjacent = set()

    def connect(self, node):
        if isinstance(node, Node):
            self.adjacent.add(node)
        else:
            raise NotImplementedError('invalid node type: {}'.format(type(node)))

    def __iter__(self):
        for node in self.adjacent:
            yield node

    def __hash__(self):
        return hash((self.number,))

    def __repr__(self):
        return 'Node({})'.format(self.number)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.number == other.number
        raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, Node):
            return self.number < other.number
        raise NotImplementedError


class Maze(object):
    POS_NODE_HOR = 0
    POS_NODE_VER = 1
    POS_TILE = 2

    def __init__(self, tile):
        self._max_rows = len(tile), len(tile) - 1, len(tile)
        self._max_cols = len(tile[0]) - 1, len(tile[0]), len(tile[0])
        self._tiles = tile
        self._nodes = self._init_nodes()
        self._init_node_connections()

    def get_tile(self, row, col):
        if self._valid_tile_position(row, col):
            return self._tiles[row][col]
        return None

    def get_node(self, n_type, row, col):
        if self._valid_node_position(n_type, row, col):
            return self._nodes[n_type][row][col]
        return None

    def iter_nodes(self):
        for t in range(2):
            for r in range(self._max_rows[t]):
                for c in range(self._max_cols[t]):
                    yield self._nodes[t][r][c]
        raise StopIteration

    def _init_nodes(self):
        node_number = 0
        nodes = list()
        for t in range(2):

            rows = list()
            for r in range(self._max_rows[t]):

                cols = list()
                for c in range(self._max_cols[t]):
                    node = Node(node_number)
                    node_number += 1
                    cols.append(node)

                rows.append(cols)

            nodes.append(rows)

        return nodes

    def _init_node_connections(self):
        for r in range(self._max_rows[self.POS_TILE]):
            for c in range(self._max_cols[self.POS_TILE]):
                t_ver = self.POS_NODE_VER
                t_hor = self.POS_NODE_HOR

                node_up_pos = (t_ver, r - 1, c)
                node_down_pos = (t_ver, r, c)
                node_left_pos = (t_hor, r, c - 1)
                node_right_pos = (t_hor, r, c)

                node_up = self.get_node(*node_up_pos)
                node_down = self.get_node(*node_down_pos)
                node_left = self.get_node(*node_left_pos)
                node_right = self.get_node(*node_right_pos)

                tile = self.get_tile(r, c)

                if tile == '/':
                    # connect (up, left) (down, right)
                    if node_up and node_left:
                        node_up.connect(node_left)
                        node_left.connect(node_up)

                    if node_down and node_right:
                        node_down.connect(node_right)
                        node_right.connect(node_down)

                elif tile == '\\':
                    # connect (up, right) (down, left)
                    if node_up and node_right:
                        node_up.connect(node_right)
                        node_right.connect(node_up)

                    if node_down and node_left:
                        node_down.connect(node_left)
                        node_left.connect(node_down)

                else:
                    raise ValueError('invalid tile value ({} {}): {}'.format(r, c, tile))

    def _valid_tile_position(self, row, col):
        return (0 <= row < self._max_rows[self.POS_TILE]) and \
               (0 <= col < self._max_cols[self.POS_TILE])

    def _valid_node_position(self, node_type, row, col):
        return node_type in (self.POS_NODE_HOR, self.POS_NODE_VER) and \
               (0 <= row < self._max_rows[node_type]) and \
               (0 <= col < self._max_cols[node_type])


def iter_dfs(src):
    visited = set()
    stack = list([src])

    while stack:
        current = stack.pop()
        visited.add(current)

        for neighbor in current:
            if neighbor not in visited:
                stack.append(neighbor)

    return visited


def solution(maze):
    complete_cycles = list()
    visited = set()
    for src_node in maze.iter_nodes():
        if src_node not in visited:

            cycle = iter_dfs(src_node)
            visited.update(cycle)

            if len(cycle) >= 4:
                is_cycle = True
                for node in cycle:
                    if len(node.adjacent) != 2:
                        is_cycle = False
                        break

                if is_cycle:
                    complete_cycles.append(len(cycle))

    return complete_cycles


def load():
    while True:
        width, height = next(stdin).split()
        width, height = int(width), int(height)
        if width == 0 and height == 0:
            raise StopIteration

        rows = list()
        for h in range(height):
            cols = next(stdin)[:width]
            rows.append(cols)
        yield Maze(rows)


def main():
    for case_num, maze in enumerate(load(), start=1):
        cycles = solution(maze)

        print('Maze #{}:'.format(case_num))
        if cycles:
            print('{cycle_count} Cycles; the longest has length {max_cycle}.'.format(
                cycle_count=len(cycles), max_cycle=max(cycles)))
        else:
            print('There are no cycles.')
        print()


if __name__ == '__main__':
    main()
