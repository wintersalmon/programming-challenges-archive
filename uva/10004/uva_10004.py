"""
Bicoloring
Uva: 10004
programming-challenges Chapter09 PR_065

# how to solve
1. start from any node[0] and paint with color_1
2. if node is not painted yet
    1. paint current node
    2. paint all child with different color
    3. return True if all child paint was success
3. if node is already painted with same color return True
4. if node is already painted with different color return False

"""
from sys import stdin

COLOR_WHITE = 1
COLOR_BLACK = 2
FLIP_COLOR = 3


def flip_color(color):
    return color ^ FLIP_COLOR


def read_input():
    while True:
        num_of_nodes = int(next(stdin))
        if num_of_nodes == 0:
            raise StopIteration

        num_of_edges = int(next(stdin))

        edges = list()
        for i in range(num_of_edges):
            s, d = next(stdin).split()
            edge = (int(s), int(d))
            edges.append(edge)

        yield num_of_nodes, edges


class Node(object):
    def __init__(self, name):
        self.name = name
        self.color = None
        self.child = set()

    def add_node(self, node):
        self.child.add(node)

    def set_color(self, color):
        self.color = color

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.__str__()


class Graph(object):
    def __init__(self, n, edges):
        self.nodes = [Node(i) for i in range(n)]

        for s, d in edges:
            src_node = self.nodes[s]
            dst_node = self.nodes[d]
            src_node.add_node(dst_node)


def solution(n, edges):
    graph = Graph(n, edges)
    result = travel(graph.nodes[0], COLOR_BLACK)
    return result


def travel(cur_node, color):
    if cur_node.color is None:
        cur_node.color = color
        for child in cur_node.child:
            # if any of the child fails to paint exit searching
            if not travel(child, flip_color(color)):
                return False

        return True
    elif cur_node.color == color:
        return True
    else:  # cur_node.color != color
        return False


def main():
    for n, edges in read_input():
        if solution(n, edges):
            print('BICOLORABLE.')
        else:
            print('NOT BICOLORABLE.')


if __name__ == '__main__':
    main()
