"""
The Tourist Guide
Uva: 10099
programming-challenges Chapter09 PR_067

다익스트라 알고리즘의 변형 문제
1. 최단거리가 아닌 최대 운송 값을 구한다
3. 경로의 weight 누적값이 아닌 경로상 최소 weight 를 이용한다

1. 그래프를 생성한다 (weight 값에서 1을 미리 빼준다, 가이드가 버스에 함께 타야하기 때문에)
2. 시작점으로 부터 인접 노드를 순회한다 (heapq, reversed-child-iter 를 이용해서 가장 큰 weight 를 가지는 노드를 우선으로 방문한다)
    - 다음 노드의 weight 값이 math.inf 인 경우 값을 갱신한다
    - 다음 노드의 weight 값이 이전 노드의 weight 값보다 작을경우 값을 갱신한다

"""

import heapq
import math
from sys import stdin

DEBUG_MODE = False


class Node(object):
    NODE = 0
    WEIGHT = 1

    def __init__(self, value):
        self.value = value
        self.children = list()

    def add_child(self, child, weight):
        self.children.append((child, weight))

    def __iter__(self):
        for child, weight in sorted(self.children, key=lambda x: x[self.WEIGHT], reverse=True):
            yield child, weight

    def __repr__(self):
        return 'Node({})'.format(self.value)

    def __hash__(self):
        return hash((self.value,))

    def __lt__(self, other):
        if isinstance(other, Node):
            return self.value < other.value
        elif isinstance(other, int):
            return self.value < other
        raise NotImplementedError


def load():
    while True:
        num_of_nodes, num_of_edges = next(stdin).split()
        num_of_nodes, num_of_edges = int(num_of_nodes), int(num_of_edges)
        if num_of_nodes == 0 and num_of_edges == 0:
            raise StopIteration

        nodes = [Node(i) for i in range(num_of_nodes)]

        while num_of_edges > 0:
            num_of_edges -= 1

            src, dst, weight = next(stdin).split()
            src, dst, weight = int(src) - 1, int(dst) - 1, int(weight) - 1  # need to add guide (-1 weight)
            if weight > 0:
                nodes[src].add_child(nodes[dst], weight)
                nodes[dst].add_child(nodes[src], weight)

        src_node, dst_node, num_of_passengers = next(stdin).split()
        src_node, dst_node, num_of_passengers = int(src_node) - 1, int(dst_node) - 1, int(num_of_passengers)

        yield nodes, src_node, dst_node, num_of_passengers


def iter_nodes_reversed_dijkstra(src):
    visited = set()
    queue = [(0, src)]
    while queue:
        _, from_node = heapq.heappop(queue)
        for to_node, weight in from_node:
            if to_node not in visited:
                heapq.heappush(queue, (-weight, to_node))
                yield from_node, to_node, weight
        visited.add(from_node)


def solution(nodes, src, dst, passengers):
    parent_node_weight = [math.inf for _ in range(len(nodes))]
    for from_node, to_node, to_node_weight in iter_nodes_reversed_dijkstra(nodes[src]):
        from_node_weight = parent_node_weight[from_node.value]
        prev_node_weight = parent_node_weight[to_node.value]
        next_node_weight = min(from_node_weight, to_node_weight)
        if prev_node_weight == math.inf or prev_node_weight < next_node_weight:
            parent_node_weight[to_node.value] = next_node_weight

    min_weight = parent_node_weight[dst]

    if DEBUG_MODE:
        print(len(nodes), src, dst, passengers)
        for node in nodes:
            print(node, *node)

        for i in range(len(nodes)):
            print('{node}: {weight_from_root}'.format(node=i, weight_from_root=parent_node_weight[i]))

    return math.ceil(passengers / min_weight)


def main():
    for i, values in enumerate(load(), 1):
        min_num_of_trips = solution(*values)
        print('Scenario #{}'.format(i))
        print('Minimum Number of Trips = {}'.format(min_num_of_trips))
        print()


if __name__ == '__main__':
    main()


# def min_weight_within_path(weights, path):
#     return min(map(lambda x: weights[x], path))
#
#
# def find_path_to_root(parent_node, src):
#     path = list()
#     parent = src
#     while parent is not None:
#         path.append(parent)
#         parent = parent_node[parent]
#     return list(reversed(path))
#
#
# def find_min_path_weight(parent_node, parent_node_weight, src):
#     path = find_path_to_root(parent_node, src)
#     return min_weight_within_path(parent_node_weight, path)
#
#
# def solution(nodes, src, dst, passengers):
#     parent_node = [None for _ in range(len(nodes))]
#     parent_node_weight = [math.inf for _ in range(len(nodes))]
#     visited = set()
#
#     not_visited_heapq = [(-passengers, src)]
#     heapq.heapify(not_visited_heapq)
#     while not_visited_heapq:
#         _, from_node = heapq.heappop(not_visited_heapq)
#         from_node_weight = find_min_path_weight(parent_node, parent_node_weight, from_node)
#
#         for to_node, to_node_weight in nodes[from_node]:
#             to_node_idx = to_node.value
#             if to_node_idx in visited:
#                 continue
#
#             prev_node_weight = find_min_path_weight(parent_node, parent_node_weight, to_node_idx)
#             next_node_weight = min(from_node_weight, to_node_weight)
#             heapq.heappush(not_visited_heapq, (-to_node_weight, to_node_idx))
#
#             if parent_node_weight[to_node_idx] == math.inf:
#                 parent_node[to_node_idx] = from_node
#                 parent_node_weight[to_node_idx] = next_node_weight
#             elif prev_node_weight < next_node_weight:
#                 parent_node[to_node_idx] = from_node
#                 parent_node_weight[to_node_idx] = next_node_weight
#
#         visited.add(from_node)
#
#     min_path = find_path_to_root(parent_node, dst)
#     min_weight = min(math.inf, min_weight_within_path(parent_node_weight, min_path))
#
#     if DEBUG_MODE:
#         print(len(nodes), src, dst, passengers)
#         for node in nodes:
#             print(node, *node)
#
#         for i in range(len(nodes)):
#             print('{prev} -> {cur}: {weight}'.format(cur=i, prev=parent_node[i], weight=parent_node_weight[i]))
#
#         prev_n = min_path[0]
#         for next_n in min_path[1:]:
#             print('{prev} -> {cur}: {weight} {node}'.format(prev=prev_n, cur=next_n, weight=parent_node_weight[next_n],
#                                                             node=nodes[prev_n]._children))
#             prev_n = next_n
#
#         print(min_path, min_weight)
#
#     return math.ceil(passengers / min_weight)
#
#
# def solution2(nodes, src, dst, passengers):
#     parent_node_weight = [math.inf for _ in range(len(nodes))]
#     visited = set()
#
#     not_visited_heapq = [(-passengers, src)]
#     heapq.heapify(not_visited_heapq)
#     while not_visited_heapq:
#         _, from_node = heapq.heappop(not_visited_heapq)
#         from_node_weight = parent_node_weight[from_node]
#
#         for to_node, to_node_weight in nodes[from_node]:
#             to_node_idx = to_node.value
#             if to_node_idx not in visited:
#                 heapq.heappush(not_visited_heapq, (-to_node_weight, to_node_idx))
#
#                 prev_node_weight = parent_node_weight[to_node_idx]
#                 next_node_weight = min(from_node_weight, to_node_weight)
#
#                 if prev_node_weight == math.inf or prev_node_weight < next_node_weight:
#                     parent_node_weight[to_node_idx] = next_node_weight
#
#         visited.add(from_node)
#
#     min_weight = parent_node_weight[dst]
#
#     return math.ceil(passengers / min_weight)
