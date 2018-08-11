"""
Playing With Wheels
Uva: 10067
programming-challenges Chapter09 PR_066



"""

from sys import stdin

import collections


def read_and_convert_to_int(line):
    return int(line)


def read_and_convert_into_tuple(num_in_string):
    return tuple(int(n) for n in num_in_string.split())


def read_input():
    num_of_cases = read_and_convert_to_int(next(stdin))

    while num_of_cases > 0:

        num_of_cases -= 1

        start_number = read_and_convert_into_tuple(next(stdin))
        target_number = read_and_convert_into_tuple(next(stdin))
        banned_number_count = read_and_convert_to_int(next(stdin))

        banned_numbers = set()
        for i in range(banned_number_count):
            banned_numbers.add(read_and_convert_into_tuple(next(stdin)))

        yield start_number, target_number, banned_numbers

        next(stdin)  # read empty line

    raise StopIteration


class Node(object):
    def __init__(self, value):
        self.value = value
        self._children = set()

    def add_child(self, child):
        self._children.add(child)

    def _compare(self, other):
        if isinstance(other, Node):
            return self.value == other.value
        elif isinstance(other, self.value):
            return self.value == other
        raise NotImplementedError

    def __iter__(self):
        for child in self._children:
            yield child

    def __hash__(self):
        return hash((self.value,))

    def __eq__(self, other):
        return self._compare(other)

    def __ne__(self, other):
        return not self._compare(other)


def create_number_graph():
    movements = [
        lambda x: ((x[0] + 1) % 10, x[1], x[2], x[3]),
        lambda x: ((x[0] - 1) % 10, x[1], x[2], x[3]),

        lambda x: (x[0], (x[1] + 1) % 10, x[2], x[3]),
        lambda x: (x[0], (x[1] - 1) % 10, x[2], x[3]),

        lambda x: (x[0], x[1], (x[2] + 1) % 10, x[3]),
        lambda x: (x[0], x[1], (x[2] - 1) % 10, x[3]),

        lambda x: (x[0], x[1], x[2], (x[3] + 1) % 10),
        lambda x: (x[0], x[1], x[2], (x[3] - 1) % 10),
    ]

    graph = dict()

    for a in range(10):
        for b in range(10):
            for c in range(10):
                for d in range(10):
                    value = (a, b, c, d)
                    if value not in graph:
                        graph[value] = Node(value=value)
                    node = graph[value]

                    for move in movements:
                        child_value = move(value)
                        if child_value not in graph:
                            graph[child_value] = Node(value=child_value)
                        child = graph[child_value]
                        node.add_child(child)

    return graph


def iter_bfs(visited, src):
    """iter graph with bfs, yield (vertex, child) until all node is visited"""
    queue = collections.deque([src])

    while queue:
        vertex = queue.popleft()

        for child in vertex:
            if child not in visited:
                visited.add(child)
                queue.append(child)

                yield vertex, child
    else:
        raise StopIteration


def iter_dfs(visited, src):
    """iter graph with dfs, yield (vertex, child) until all node is visited"""
    queue = list()
    queue.append(src)

    while queue:
        vertex = queue.pop()

        for child in vertex:
            if child not in visited:
                visited.add(child)
                queue.append(child)

                yield vertex, child
    else:
        raise StopIteration


def solution(graph, src, dst, banned):
    src = graph[src]
    dst = graph[dst]

    visited = set()

    visited.add(src)
    for b in banned:
        visited.add(graph[b])

    steps = dict()
    steps[src] = 0

    for from_node, to_node in iter_bfs(visited, src):
        steps[to_node] = steps[from_node] + 1

    if dst in steps:
        return steps[dst]
    else:
        return -1


def main():
    graph = create_number_graph()
    for src, dst, banned in read_input():
        print(solution(graph, src, dst, banned))


if __name__ == '__main__':
    main()
    # solution(_tools=(8, 0, 5, 6),
    #          dst=(6, 5, 0, 8),
    #          banned={
    #              (8, 0, 5, 7),
    #              (8, 0, 4, 7),
    #              (5, 5, 0, 8),
    #              (7, 5, 0, 8),
    #              (6, 4, 0, 8),
    #          })
