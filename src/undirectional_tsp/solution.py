from sys import stdin

COST = 0
PATH = 1


def load():
    while True:
        line = next(stdin)
        row_count_str, col_count_str = line.split()
        row_count, col_count = int(row_count_str), int(col_count_str)
        total_count = row_count * col_count

        items = list()
        while len(items) < total_count:
            row = next(stdin)
            cols = row.split()
            cur_items = [int(col) for col in cols]
            items += cur_items

        rows = list()
        while items:
            row = items[:col_count]
            rows.append(row)
            items = items[col_count:]

        yield rows


def print_answer_in_format(nodes, cost):
    nodes_in_str = [str(node + 1) for node in nodes]
    print(' '.join(nodes_in_str))
    print(cost)


class Path(object):
    def __init__(self):
        self.nodes = list()
        self.cost = 0

    def move(self, next_node, next_cost):
        self.nodes.append(next_node)
        self.cost += next_cost

    def clone(self):
        path = Path()
        path.nodes = self.nodes
        path.cost = self.cost
        return path

    def __repr__(self):
        return '{} : {}'.format(self.nodes, self.cost)


def find_prev_shortest_path(board, prev_shortest_values, cur_row_idx, cur_col_idx):
    # the previous path can be one of (up_left, left, down_left)
    # create next path with each previous (cost, path)
    # find and return shortest (cost, path)
    prev_col_idx = cur_col_idx - 1
    up_row_idx = cur_row_idx - 1 if cur_row_idx > 0 else len(board) - 1
    mid_row_idx = cur_row_idx
    down_row_idx = (cur_row_idx + 1) % len(board)

    up_cost = prev_shortest_values[up_row_idx][prev_col_idx][COST]
    mid_cost = prev_shortest_values[cur_row_idx][prev_col_idx][COST]
    down_cost = prev_shortest_values[down_row_idx][prev_col_idx][COST]

    row_cost_pairs = [
        (up_cost, prev_shortest_values[up_row_idx][prev_col_idx][PATH] + [cur_row_idx]),
        (mid_cost, prev_shortest_values[mid_row_idx][prev_col_idx][PATH] + [cur_row_idx]),
        (down_cost, prev_shortest_values[down_row_idx][prev_col_idx][PATH] + [cur_row_idx]),
    ]

    row_cost_pairs.sort()

    shortest_path = row_cost_pairs[0][PATH]
    shortest_path_cost = row_cost_pairs[0][COST]

    return shortest_path, shortest_path_cost


def search_shortest_path(board):
    row_size = len(board)
    col_size = len(board[0])

    # create data structures
    accumulated_costs = board[:]
    accumulated_paths = [[[row_idx] for _ in range(col_size)] for row_idx in range(row_size)]
    accumulated_values = [[[accumulated_costs[r][c], accumulated_paths[r][c]]
                           for c in range(col_size)] for r in range(row_size)]

    # for each row in each colon, increment each path with shortest previous path
    for col_idx in range(1, col_size):
        for row_idx in range(row_size):
            shortest_path, shortest_cost = find_prev_shortest_path(board, accumulated_values, row_idx, col_idx)
            accumulated_values[row_idx][col_idx][PATH] = shortest_path
            accumulated_values[row_idx][col_idx][COST] = shortest_cost + accumulated_values[row_idx][col_idx][COST]

    # select last colon and sort them with (cost, path) order
    last_values = [(values[-1][COST], values[-1][PATH]) for values in accumulated_values]
    last_values.sort()

    return last_values[0][PATH], last_values[0][COST]


def main():
    for board in load():
        nodes, cost = search_shortest_path(board)
        print_answer_in_format(nodes, cost)


if __name__ == '__main__':
    main()
