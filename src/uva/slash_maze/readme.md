# Slash Maze
- Uva: 705
- Programming Challenges Problem 68 (Chapter 09)


# Solution

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

    (n, m) tile
    [n, m] node_hor
    <n, m> node_ver

    (0 0)   [0 0]   (0 1)   [0 1]   (0 2)

    <0 0>           <0 1>           <0 2>

    (1 0)   [1 0]   (1 1)   [1 1]   (1 2)

    <1 0>           <1 1>           <1 2>

    (2 0)   [2 0]   (2 1)   [2 1]   (2 2)


### convert tile coordinate to adjacent node coordinate


    tile        n, m
    node_up     n - 1, m
    node_right  n, m
    node_down   n, m
    node_left   n, m - 1


                <n-1, m>

    [n, m-1]    (n, m)      [n, m]

                <n, m>